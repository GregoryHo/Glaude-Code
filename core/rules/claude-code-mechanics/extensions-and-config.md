# Extensions & Config Mechanics

## MCP Servers

- `claude mcp add` — 3 scopes:
  - **local** (default): project-specific, stored in `~/.claude.json`
  - **project**: `.mcp.json` in project root (version controlled, shared with team)
  - **user**: `~/.claude.json` global entry (available across all projects)
- MCP tools appear as `mcp__<server>__<tool>` in hook events and tool lists
- Precedence: local > project > user
- WRONG: "MCP configured in ~/.claude/mcp-config.json" — use `claude mcp add` with scopes

## Settings Hierarchy (highest to lowest)

1. Managed policy (system-wide, cannot be overridden)
2. Command-line arguments
3. `.claude/settings.local.json` (project-local, gitignored)
4. `.claude/settings.json` (project-shared, version controlled)
5. `~/.claude/settings.json` (user global)

More specific scopes override broader ones.

## Plugins

- Enabled in `settings.json`
- Bundle hooks + skills + MCP servers into a single package
- Scoped to settings hierarchy like everything else
