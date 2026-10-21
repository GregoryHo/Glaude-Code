"""Resolve one workspace/server and exec the existing bridge without a shell.

No MCP proxy, installation, project commands, or global configuration writes.
Automatic detection intentionally rejects ambiguous and unrecognized projects.
"""
import argparse
import json
import os
from pathlib import Path
import sys


LANGUAGES = ('typescript', 'python', 'rust', 'go', 'kotlin', 'swift')
MARKERS = {
    'typescript': ('package.json', 'tsconfig.json', 'jsconfig.json'),
    'python': ('pyproject.toml', 'pyrightconfig.json', 'setup.py'),
    'rust': ('Cargo.toml',),
    'go': ('go.mod', 'go.work'),
    'kotlin': ('build.gradle.kts', 'settings.gradle.kts'),
    'swift': ('Package.swift',),
}


def workspace(explicit, host, cwd, env):
    if explicit:
        value, origin = explicit, 'explicit'
    elif host == 'claude':
        value, origin = env.get('CLAUDE_PROJECT_DIR'), 'CLAUDE_PROJECT_DIR'
        if not value:
            raise ValueError('Claude did not provide CLAUDE_PROJECT_DIR; supply --workspace explicitly')
    else:
        value, origin = str(cwd), 'process-cwd'
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError(f'Workspace must be absolute ({origin}): {value}')
    path = path.resolve(strict=True)
    if not path.is_dir() or path in (Path('/'), Path.home().resolve()):
        raise ValueError(f'Refusing non-project workspace: {path}')
    # Keep the exact host boundary; do not walk upward into another project.
    return path, origin


def language_for(root, selected):
    if selected != 'auto':
        return selected
    found = [name for name, markers in MARKERS.items() if any((root / m).is_file() for m in markers)]
    if len(found) != 1:
        raise ValueError(f'Cannot select one server for {root}: found {found}; use --language explicitly')
    return found[0]


def executable(value, label, root):
    if not isinstance(value, str) or not Path(value).is_absolute():
        raise ValueError(f'{label} must be an absolute executable path')
    path = Path(value).resolve(strict=True)
    if path.is_relative_to(root):
        raise ValueError(f'{label} must not come from the target workspace: {path}')
    if not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError(f'{label} is not executable: {path}')
    return str(path)


def plan(config, root, language, origin, lazy=False):
    bridge = executable(config.get('bridge'), 'bridge', root)
    server = config.get('servers', {}).get(language)
    if not isinstance(server, dict):
        raise ValueError(f'No trusted server entry for {language}')
    binary = executable(server.get('command'), f'{language} server', root)
    args = server.get('args', [])
    if not isinstance(args, list) or any(not isinstance(a, str) for a in args):
        raise ValueError(f'{language} server args must be a string array')
    return {'workspace': str(root), 'workspace_source': origin, 'language': language,
            'argv': [bridge, '--workspace', str(root), '--lsp', binary,
                     *(['--lazy'] if lazy else []), '--', *args]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', required=True, choices=('codex', 'claude'))
    parser.add_argument('--workspace', help='Explicit absolute workspace; overrides host discovery')
    parser.add_argument('--language', default='auto', choices=('auto', *LANGUAGES))
    parser.add_argument('--config', required=True, help='Absolute trusted user-owned server-map JSON')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--lazy', action='store_true', help='Require a bridge supporting on-demand LSP startup')
    args = parser.parse_args()
    try:
        root, origin = workspace(args.workspace, args.host, Path.cwd(), os.environ)
        config_path = Path(args.config)
        if not config_path.is_absolute():
            raise ValueError('--config must be an absolute path')
        config_path = config_path.resolve(strict=True)
        if config_path.is_relative_to(root):
            raise ValueError('Server map must be outside the target workspace')
        config = json.loads(config_path.read_text())
        if not isinstance(config, dict):
            raise ValueError('Server map must be a JSON object')
        result = plan(config, root, language_for(root, args.language), origin, args.lazy)
        if args.dry_run:
            print(json.dumps(result, indent=2))
            return
        print(f"retrieval-lsp: {result['language']} workspace={root} source={origin}", file=sys.stderr)
        os.chdir(root)
        os.execv(result['argv'][0], result['argv'])
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        print(f'retrieval-lsp: {exc}', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
