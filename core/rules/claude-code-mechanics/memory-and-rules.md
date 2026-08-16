# Memory & Rules Mechanics

## Rules

- `~/.claude/rules/*.md` (user) and `.claude/rules/*.md` (project) **auto-load** — no registration needed
- Recursive `.md` discovery — subdirectories work (e.g. `rules/frontend/react.md`)
- `paths:` frontmatter scopes a rule to matching files — documented for both project and user level. Behavior has churned across versions (GH #21858, #19377, #17204: YAML-array vs CSV parsing, quoting); don't trust any single report. Verify on the current version with `/context` → **Memory files**, or the `InstructionsLoaded` hook
- Path-scoped rules load when Claude **reads a matching file**, not at launch — and are **not re-injected after compaction**. Don't path-scope behavioral guidance that must apply from turn one
- WRONG: "rules files need a one-liner in CLAUDE.md for discoverability" — they auto-load

## CLAUDE.md Hierarchy (highest to lowest)

1. Managed policy (`/Library/Application Support/ClaudeCode/CLAUDE.md`)
2. Project (`./CLAUDE.md` or `./.claude/CLAUDE.md`) — full load at launch
3. Project rules (`.claude/rules/*.md`) — recursive, full load at launch
4. User global (`~/.claude/CLAUDE.md`) — full load at launch
5. Project local (`./CLAUDE.local.md`) — gitignored, full load at launch
6. Auto-memory (`MEMORY.md` first 200 lines only)
7. Child-dir CLAUDE.md — loaded **on-demand** when accessing that directory

- `CLAUDE.local.md` = personal project prefs, auto-gitignored

## Auto-Memory

- Lives at `~/.claude/projects/<project-hash>/memory/`
- Only `MEMORY.md` first 200 lines load at startup into system prompt
- Topic files (`debugging.md`, etc.) exist but load **on-demand** when Claude reads them
- WRONG: "auto-memory loads all files at startup" — only MEMORY.md, only first 200 lines
