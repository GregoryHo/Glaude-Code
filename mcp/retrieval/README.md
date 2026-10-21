# Personal retrieval setup — 0.2.0

Cloning Glaude-Code copies instructions, not a compiled LSP bridge or language
servers. This installer builds the fork pinned in `manifest.json` and generates
paths for this Mac. No sibling harness checkout or previous user's home is needed.

## New Mac

Requirements: macOS, Git, Go 1.24+, Python 3.11+, and the chosen native servers.
Homebrew is needed only for the optional dependency recipes. With Homebrew:
`brew install python go`. If `python3` is an older system interpreter, use the
Python installed by Homebrew, or set `GLAUDE_PYTHON` when running `install.sh`.

From the cloned Glaude-Code directory:

```sh
python3 mcp/retrieval/installer.py doctor
python3 mcp/retrieval/installer.py install --languages typescript,python --install-missing
python3 mcp/retrieval/installer.py configure --host both --dry-run
python3 mcp/retrieval/installer.py configure --host both
```

Doctor is read-only and exits 1 for missing components. It reports executables,
missing tools, install commands, and installed version/commit, not environment
variables or credentials. `install` defaults to detected language servers;
`--languages all` requests all six families. `--install-missing` explicitly
authorizes dependency installation. Otherwise missing selected dependencies fail
with commands rather than silently configuring broken servers.

The optional LSP prompt in `./install.sh` runs the same flow. Restart the host
session after configuration. Claude uses the injected `CLAUDE_PROJECT_DIR`;
Codex uses process cwd. A later shell `cd` does not switch an existing instance.

## Dependencies

| Family | Native server | Missing dependency recipe |
| --- | --- | --- |
| JavaScript / TypeScript | typescript-language-server + TypeScript + Node | Homebrew Node if absent, then npm global typescript and typescript-language-server |
| Python | Microsoft's pyright-langserver + Node | `brew install pyright` |
| Rust | rust-analyzer in the local Rust toolchain | `rustup component add rust-analyzer rust-src` (install rustup first if absent) |
| Go | gopls + Go | Homebrew Go if absent, then `go install golang.org/x/tools/gopls@latest` |
| Kotlin | Official Kotlin LSP | `brew install JetBrains/utils/kotlin-lsp` |
| Swift | sourcekit-lsp from the selected Xcode toolchain | Install/select Xcode manually; the installer never installs Xcode |

Native package recipes use the package manager's current release; installed
versions are recorded, not claimed identical across machines. Existing tools
are reused. Binary locations are resolved on each Mac, including Node script
entrypoints, Rust's proxy, and Homebrew prefixes. Node is invoked explicitly for
Node-based servers so GUI sessions do not depend on the login shell's Node PATH.
Toolchain upgrades can invalidate installed paths: run doctor, install, configure
again. Missing Swift is reported and skipped; Kotlin/Xcode project semantics
remain limited even when the executable exists.

## Files and updates

Runtime files live under `~/.local/share/agent-retrieval-harness/`:
`installation.json` records the source commit, version, artifact hashes, native
versions/paths, Python interpreter, and installed languages. Each release holds
the bridge, launcher, and server map. Build source is fetched at the fixed commit
in a temporary checkout. `--source /path/to/bridge-repo` is a developer option;
it still fetches and verifies the pinned commit, ignoring uncommitted changes.

Configure merges only selected `lsp_*` entries into `~/.claude.json` and/or
`~/.codex/config.toml`. Claude permissions in `~/.claude/settings.json` allow the
four retrieval tools and deny the four legacy/mutation tools. The mgrep plugin
is disabled there. Codex uses a four-tool catalog allowlist. Native language
servers are not sandboxed by these settings.

Conflicting LSP entries show a transport diff and require confirmation; scripted
replacement uses `--yes` after reviewing `--dry-run`. Settings backups are stored
in private `.retrieval-backups` directories beside the originals. Configuration
parsing and all conflict decisions happen before writing. Each file is replaced
atomically, with a concurrent-change check; this is not a multi-file transaction.
Repeated configure is a no-op. Selecting fewer languages does not delete earlier
instances; disable unwanted entries explicitly. Unsupported TOML layouts fail
before writing instead of rewriting unrelated settings/comments.

Default paths are per-user. Codex installations using a custom `CODEX_HOME` must
configure their alternate config manually; this installer targets `~/.codex`.

## Search policy and approval

[ROUTING.md](ROUTING.md) is the shared policy. `sync_policy.py --write` refreshes
the two repository instruction templates; add `--deploy` to refresh live user
instructions. Plain `sync_policy.py` checks consistency without writing.

For mgrep, a user can authorize a repo in its agent instructions, for example:

```text
User-approved mgrep scope: this repository, directories src/ and tests/ only.
Remote indexing and processing of these directories are permitted.
Use on-demand queries/sync within that scope; do not start a watcher.
```

This is a template, not authorization. Do not enable the old mgrep plugin/MCP
or index any repo as part of LSP setup. Semgrep is a separate local CLI; this
installer does not install security rules, log in, or register a security MCP.

## Verification

```sh
python3 -m unittest discover -s mcp/retrieval -v
python3 mcp/retrieval/sync_policy.py
```

Run `smoke.py --root <installation-root>` for two real TypeScript/Python MCP
definition queries in disposable fixtures. It does not call a model or alter
host settings. Then use the same queries in a new CLI session to verify the
host connection: `main.ts` 2:16 and `main.py` 3:10, expecting definition ranges
L1:C1–L1:C60 and L1:C1–L2:C21 respectively. Use the fixtures printed by the
smoke script with `--keep-fixture` to retain them for host queries; by default
it deletes them on completion. After host checks, remove only that printed
synthetic fixture directory.

Actual migration acceptance requires running the install and two queries on the
second Mac. Local simulated paths do not establish Intel hardware compatibility
or seven-language project semantics. See VALIDATION.md for recorded results.

References: [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp),
[Claude MCP](https://code.claude.com/docs/en/mcp),
[Pyright](https://github.com/microsoft/pyright/blob/main/docs/installation.md),
[Kotlin LSP](https://github.com/Kotlin/kotlin-lsp).
