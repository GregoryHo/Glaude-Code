#!/usr/bin/env python3
"""Install the pinned personal LSP bridge and merge host-local configuration."""
import argparse
import copy
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
try:
    import tomllib
except ImportError:
    raise SystemExit('Python 3.11+ is required; on macOS: brew install python')

HERE = Path(__file__).resolve().parent
LANGUAGES = ('typescript', 'python', 'rust', 'go', 'kotlin', 'swift')
TOOLS = ('definition_at', 'references_at', 'hover', 'diagnostics')
DENIED = ('definition', 'references', 'edit_file', 'rename_symbol')
BINARIES = dict(zip(LANGUAGES, ('typescript-language-server', 'pyright-langserver',
                               'rust-analyzer', 'gopls', 'kotlin-lsp', 'sourcekit-lsp')))
DEFAULT_ROOT = Path.home()/'.local/share/agent-retrieval-harness'


def run(argv, **kwargs):
    return subprocess.run([str(a) for a in argv], check=True, text=True,
                          stdin=subprocess.DEVNULL, **kwargs)


def output(argv, timeout=10):
    try:
        return run(argv, capture_output=True, timeout=timeout).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def resolve_binary(name):
    found = shutil.which(name)
    if not found:
        return None
    path = Path(found).resolve()
    if name == 'rust-analyzer' and path.name == 'rustup':
        found = output([str(path), 'which', 'rust-analyzer'], timeout=5)
        if not found:
            return None
        path = Path(found).resolve()
    return str(path) if path.is_file() and os.access(path, os.X_OK) else None


def discover():
    entries, missing = {}, {}
    node = resolve_binary('node')
    for language, name in BINARIES.items():
        binary = resolve_binary(name)
        if language == 'swift':
            located = output(['xcrun', '--find', 'sourcekit-lsp'])
            binary = str(Path(located).resolve()) if located else binary
        if language == 'go' and not binary:
            gopath = output(['go', 'env', 'GOPATH'])
            if gopath:
                candidate = Path(gopath.split(os.pathsep)[0])/'bin/gopls'
                if candidate.is_file() and os.access(candidate, os.X_OK):
                    binary = str(candidate.resolve())
        if not binary:
            missing[language] = f'{name} not found'
            continue
        args = ['--stdio'] if language in ('typescript', 'python', 'kotlin') else []
        if language == 'go':
            args = ['serve']
        # Avoid /usr/bin/env node depending on a GUI host's reduced PATH.
        if language in ('typescript', 'python'):
            if not node:
                missing[language] = 'Node.js runtime not found'
                continue
            if language == 'typescript' and not resolve_binary('tsc'):
                missing[language] = 'TypeScript compiler (tsc) not found'
                continue
            with Path(binary).open('rb') as handle:
                first = handle.readline(256)
            if b'node' in first or Path(binary).suffix in ('.js', '.mjs', '.cjs'):
                args = [binary, *args]
                binary = node
        entries[language] = {'command': binary, 'args': args}
    return entries, missing


def recipes(language):
    return {
        'typescript': [['brew', 'install', 'node'], ['npm', 'install', '-g', 'typescript', 'typescript-language-server']],
        'python': [['brew', 'install', 'pyright']],
        'rust': [['rustup', 'component', 'add', 'rust-analyzer', 'rust-src']],
        'go': [['brew', 'install', 'go'], ['go', 'install', 'golang.org/x/tools/gopls@latest']],
        'kotlin': [['brew', 'install', 'JetBrains/utils/kotlin-lsp']],
        'swift': [],
    }[language]


def selected_languages(value, detected):
    if value is None:
        names = list(detected)
    else:
        names = list(LANGUAGES) if value == 'all' else value.replace(',', ' ').split()
    if not names or any(n not in LANGUAGES for n in names):
        raise ValueError('Select languages: ' + ', '.join(LANGUAGES) + ' (JS uses typescript)')
    return list(dict.fromkeys(names))


def atomic_write(path, text, expected=None):
    """Private backup and atomic replacement; refuse concurrent configuration drift."""
    path = Path(path)
    if path.is_symlink():
        raise ValueError(f'Refusing to replace symlink: {path}')
    current = path.read_text() if path.exists() else ''
    if expected is not None and current != expected:
        raise ValueError(f'File changed since inspection: {path}; rerun configure')
    if current == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.parent/'.retrieval-backups'
        backup.mkdir(mode=0o700, exist_ok=True)
        os.chmod(backup, 0o700)
        with tempfile.NamedTemporaryFile(dir=backup, prefix=path.name+'.', delete=False) as handle:
            handle.write(path.read_bytes())
        print(f'Backup: {handle.name}')
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
        try:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    try:
        if expected is not None and (path.read_text() if path.exists() else '') != expected:
            raise ValueError(f'File changed before replacement: {path}; rerun configure')
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False)+'\n'


def read_receipt(root):
    path = root/'installation.json'
    if not path.is_file():
        raise ValueError(f'Missing {path}; run install first')
    receipt = json.loads(path.read_text())
    for file, digest in receipt['artifacts'].items():
        target = Path(receipt['release'])/file
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Installed artifact changed: {target}; run install again')
    mapping = json.loads((Path(receipt['release'])/'servers.json').read_text())
    for language, entry in mapping['servers'].items():
        binary = Path(entry['command'])
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise ValueError(f'{language} executable missing: {binary}; rerun install after repairing the toolchain')
        if entry['args'] and Path(entry['args'][0]).is_absolute() and not Path(entry['args'][0]).is_file():
            raise ValueError(f'{language} entrypoint missing: {entry["args"][0]}; rerun install')
    return receipt


def install(args):
    if platform.system() != 'Darwin':
        raise ValueError('Installer currently supports macOS only')
    manifest = json.loads((HERE/'manifest.json').read_text())
    commit = manifest['bridge_commit']
    if not isinstance(commit, str) or not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('manifest.json needs a fixed full bridge commit SHA')
    detected, missing = discover()
    languages = selected_languages(args.languages, detected)
    for language in languages:
        if language in missing and args.install_missing:
            commands = recipes(language)
            if not commands:
                print('Swift: install/select Xcode manually; sourcekit-lsp is unavailable')
                continue
            for command in commands:
                if command[:3] == ['brew','install','node'] and resolve_binary('node'):
                    continue
                if command[:3] == ['brew','install','go'] and resolve_binary('go'):
                    continue
                if not shutil.which(command[0]):
                    raise ValueError(f'Missing {command[0]}; install it first. Required: {shlex.join(command)}')
                print('Installing dependency: '+shlex.join(command), flush=True)
                run(command, timeout=900)
    detected, missing = discover()
    unavailable = [n for n in languages if n not in detected]
    for language in unavailable:
        print(f'Unavailable {language}: {missing[language]}; '+
              ('; '.join(shlex.join(c) for c in recipes(language)) or 'Install/select Xcode manually'))
    # Swift may remain unavailable without blocking the other selected languages.
    if any(n != 'swift' for n in unavailable):
        raise ValueError('Selected language dependencies are missing; use --install-missing or install the listed tools')
    languages = [n for n in languages if n in detected]
    if not languages:
        raise ValueError('No usable selected language servers')
    for name in ('git', 'go'):
        if not shutil.which(name):
            if name == 'go' and args.install_missing and shutil.which('brew'):
                run(['brew','install','go'], timeout=900)
                continue
            raise ValueError(f'{name} is required to build the bridge; on macOS: brew install {name}')
    root = args.root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    source_manifest = {**manifest, 'servers': {n: detected[n] for n in languages},
                       'python': str(Path(sys.executable).resolve()),
                       'python_version': platform.python_version(),
                       'go_version': output(['go','version']),
                       'launcher_sha256': hashlib.sha256((HERE/'launch.py').read_bytes()).hexdigest(),
                       'machine': platform.machine()}
    identity = hashlib.sha256(json_text(source_manifest).encode()).hexdigest()[:16]
    release = root/'releases'/f"{manifest['version']}-{commit[:12]}-{identity}"
    with tempfile.TemporaryDirectory(prefix='retrieval-build-') as temp:
        source = Path(temp)/'source'
        run(['git', 'init', '-q', source], timeout=30)
        run(['git', '-C', source, 'remote', 'add', 'origin', args.source or manifest['bridge_repository']])
        run(['git', '-C', source, 'fetch', '--depth', '1', 'origin', commit], timeout=180)
        run(['git', '-C', source, 'checkout', '-q', '--detach', 'FETCH_HEAD'])
        actual = output(['git', '-C', source, 'rev-parse', 'HEAD'])
        if actual != commit:
            raise ValueError(f'Bridge revision mismatch: expected {commit}, got {actual}')
        binary = Path(temp)/'mcp-language-server'
        run(['go', 'build', '-trimpath', '-o', binary, '.'], cwd=source, timeout=300)
        help_result = subprocess.run([str(binary), '-h'], capture_output=True, text=True, timeout=10)
        if '-lazy' not in help_result.stderr+help_result.stdout:
            raise ValueError('Built bridge does not support --lazy')
        mapping = {'bridge': str(release/'mcp-language-server'), 'servers': source_manifest['servers']}
        contents = {'mcp-language-server': binary.read_bytes(),
                    'launch.py': (HERE/'launch.py').read_bytes(),
                    'servers.json': json_text(mapping).encode()}
        artifacts = {name: hashlib.sha256(data).hexdigest() for name,data in contents.items()}
        if release.exists():
            for name,digest in artifacts.items():
                if hashlib.sha256((release/name).read_bytes()).hexdigest() != digest:
                    raise ValueError(f'Existing installation differs: {release/name}; refusing overwrite')
        else:
            release.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=release.parent, prefix='.install-') as stage:
                staging = Path(stage)/'release'
                staging.mkdir()
                for name,data in contents.items():
                    (staging/name).write_bytes(data)
                (staging/'mcp-language-server').chmod(0o755)
                os.rename(staging, release)
        for language in languages:
            run([sys.executable, release/'launch.py', '--host', 'codex',
                 '--workspace', source, '--config', release/'servers.json',
                 '--language', language, '--lazy', '--dry-run'], capture_output=True, timeout=10)
    versions = {}
    for language in languages:
        entry = detected[language]
        if language in ('kotlin','swift'):
            value = (output(['brew','list','--versions','kotlin-lsp']) if language=='kotlin'
                     else output(['xcrun','swift','--version']))
        else:
            command_args = entry['args'][:1] if entry['command']==resolve_binary('node') else []
            value = output([entry['command'], *command_args, 'version' if language=='go' else '--version'])
        versions[language] = (value or 'unavailable').splitlines()[0]
    receipt = {**source_manifest, 'release': str(release), 'languages': languages,
               'versions': versions, 'artifacts': artifacts,
               'installed_at': datetime.now(timezone.utc).isoformat()}
    atomic_write(root/'installation.json', json_text(receipt))
    print(f'Installed {manifest["version"]} from {commit}: {release}')


def host_entries(receipt, host, languages):
    release = Path(receipt['release'])
    entries = {}
    for language in languages:
        entry = {'command': receipt['python'], 'args': [str(release/'launch.py'),
                 '--host', host, '--language', language, '--config', str(release/'servers.json'), '--lazy']}
        if host == 'codex':
            entry.update(enabled=True, required=False, enabled_tools=list(TOOLS),
                         default_tools_approval_mode='approve', startup_timeout_sec=30, tool_timeout_sec=90)
        entries['lsp_'+language] = entry
    return entries


def merge_codex(text, entries):
    """Retain unrelated TOML bytes; validate the complete semantic merge before writing."""
    parsed = tomllib.loads(text)
    expected = copy.deepcopy(parsed)
    expected.setdefault('mcp_servers', {}).update(entries)
    lines = text.splitlines(keepends=True)
    output_lines, skip = [], False
    for line in lines:
        match = re.match(r'^\s*\[([^\[\]\n]+)\]\s*(?:#.*)?$', line.rstrip('\n'))
        array = re.match(r'^\s*\[\[', line)
        if match:
            key = match.group(1)
            normalized = re.sub(r'[\s"\x27]', '', key)
            skip = any(normalized == 'mcp_servers.'+n or normalized.startswith('mcp_servers.'+n+'.') for n in entries)
        elif array:
            skip = False
        if not skip:
            output_lines.append(line)
    rendered = ''.join(output_lines).rstrip()+'\n\n'
    for name,entry in entries.items():
        rendered += f'[mcp_servers.{name}]\n'
        for key,value in entry.items():
            rendered += key+' = '+json.dumps(value)+'\n'
        rendered += '\n'
    if tomllib.loads(rendered) != expected:
        raise ValueError('Cannot safely merge this TOML layout; no file was written')
    return rendered


def approve_conflicts(existing, entries, yes):
    for name, entry in entries.items():
        if name not in existing or existing[name] == entry:
            continue
        # Show changed routing/permission policy, but never dump env or headers.
        fields = ('command','args','enabled','required','enabled_tools',
                  'default_tools_approval_mode','startup_timeout_sec','tool_timeout_sec')
        old = {k:existing[name][k] for k in fields if k in existing[name]}
        extras = sorted(set(existing[name])-set(fields))
        if extras:
            old['other_fields_removed'] = extras
        new = {k:entry[k] for k in fields if k in entry}
        print(''.join(difflib.unified_diff(json_text(old).splitlines(True),
                      json_text(new).splitlines(True), fromfile=name+' existing', tofile=name+' proposed')))
        if not yes and (not sys.stdin.isatty() or input(f'Replace {name}? [y/N] ').lower() != 'y'):
            raise ValueError(f'Configuration conflict: {name}; review and use --yes to replace')


def configure(args, home=None):
    home = home or Path.home()
    receipt = read_receipt(args.root.expanduser().resolve())
    languages = selected_languages(args.languages, receipt['languages'])
    if set(languages)-set(receipt['languages']):
        raise ValueError('Selected languages are not installed; run install first')
    hosts = ('claude','codex') if args.host=='both' else (args.host,)
    updates = []
    for host in hosts:
        entries = host_entries(receipt, host, languages)
        path = home/('.claude.json' if host=='claude' else '.codex/config.toml')
        original = path.read_text() if path.exists() else ''
        parsed = (json.loads(original) if original else {}) if host=='claude' else tomllib.loads(original)
        key = 'mcpServers' if host=='claude' else 'mcp_servers'
        approve_conflicts(parsed.get(key,{}), entries, args.yes or args.dry_run)
        if host == 'claude':
            parsed.setdefault(key,{}).update(entries)
            updated = json_text(parsed)
            settings_path = home/'.claude/settings.json'
            settings_text = settings_path.read_text() if settings_path.exists() else ''
            settings = json.loads(settings_text) if settings_text else {}
            permissions = settings.setdefault('permissions', {})
            for mode,tools in [('allow',TOOLS),('deny',DENIED)]:
                target = permissions.setdefault(mode,[])
                for name in entries:
                    for tool in tools:
                        item = f'mcp__{name}__{tool}'
                        if item not in target:
                            target.append(item)
            settings.setdefault('enabledPlugins',{})['mgrep@Mixedbread-Grep'] = False
            updates.append((settings_path, settings_text, json_text(settings)))
        else:
            updated = merge_codex(original, entries)
        updates.append((path, original, updated))
    # Parse all inputs, resolve all conflicts, and preflight all files before any write.
    for path,original,_ in updates:
        if path.is_symlink() or (path.read_text() if path.exists() else '') != original:
            raise ValueError(f'Configuration path changed or is a symlink: {path}')
    for path,original,updated in updates:
        if updated != original:
            print(('Would update: ' if args.dry_run else 'Updating: ')+str(path))
            if not args.dry_run:
                atomic_write(path, updated, expected=original)
        else:
            print(f'Unchanged: {path}')


def doctor(args):
    detected, missing = discover()
    pin = json.loads((HERE/'manifest.json').read_text())
    installed = None
    try:
        installed = read_receipt(args.root.expanduser().resolve())
    except (ValueError, OSError, KeyError) as exc:
        installed = {'error': str(exc)}
    selected = selected_languages(args.languages, detected) if args.languages else list(LANGUAGES)
    report = {'platform': platform.system(), 'machine': platform.machine(),
              'source_manifest': pin,
              'python': {'path':sys.executable,'version':platform.python_version()},
              'build_tools': {n:resolve_binary(n) for n in ('git','go','node','brew','rustup')},
              'launcher_source': str(HERE/'launch.py'), 'installation': installed,
              'languages': {n:(detected[n] if n in detected else {'missing':missing[n],
                'install_commands':[shlex.join(c) for c in recipes(n)]}) for n in selected},
              'host_configs': {n:str(Path.home()/p) for n,p in
                              [('claude','.claude.json'),('codex','.codex/config.toml')]}}
    print(json_text(report), end='')
    return 1 if not pin.get('bridge_commit') or 'error' in installed or any(n not in detected for n in selected) else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for action in ('doctor','install','configure'):
        command = sub.add_parser(action)
        command.add_argument('--root',type=Path,default=DEFAULT_ROOT)
        command.add_argument('--languages',help='Comma-separated language families, or all; default detected/installed')
        if action=='install':
            command.add_argument('--install-missing',action='store_true')
            command.add_argument('--source',help='Developer override: local Git repository containing the pinned commit')
        if action=='configure':
            command.add_argument('--host',choices=('claude','codex','both'),default='both')
            command.add_argument('--dry-run',action='store_true')
            command.add_argument('--yes',action='store_true',help='Replace conflicting LSP entries after showing transport diff')
    args = parser.parse_args()
    try:
        if args.action=='doctor':
            return doctor(args)
        (install if args.action=='install' else configure)(args)
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'retrieval: {exc}',file=sys.stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
