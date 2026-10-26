# Changelog

Personal development versions. Record future changes under Unreleased.

## Unreleased

- Auto-compact at about 400K tokens. The settings template computes it as
  40% of a 1M window, which assumes a 1M-context model; on a 200K model it
  fires near 80K. `install.sh` adds `model_auto_compact_token_limit = 400000`
  to `~/.codex/config.toml` unless the key is already set, leaving the rest
  of that file untouched. Codex ignores values above 90% of the model's
  window.
- Sync the settings template back from the live config: attribution off,
  `fable` advisor, per-model effort, 24-hour time, auto-mode allow and deny
  rules, and two community plugins. Drop `Write`, `Edit`, `Bash` and
  `WebFetch` from the allow list. Machine-local entries stay out: LSP
  permissions (written by the retrieval installer), the auto-mode
  environment, directory marketplaces and the status line.

## 0.2.0 — 2026-10-21

- Share explicit question-dependent retrieval routing across Claude and Codex,
  including positive mgrep selection for approved semantic queries, scoped
  fallbacks, LSP evidence limits, and local Semgrep CE operation.
- Disable the legacy mgrep plugin in the settings template, matching local policy.
- Add macOS retrieval `doctor`, `install`, and `configure` commands and an optional
  `install.sh` entry point. Build a fixed bridge commit locally; discover native
  servers and generate machine-local paths instead of copying another Mac's paths.
- Merge host configuration with conflict review, private backups, and atomic
  writes. Preserve unrelated MCP entries and permissions; configure only selected
  installed language servers with lazy startup and read-only retrieval access.

See [retrieval installation](mcp/retrieval/README.md) for requirements and limits.
