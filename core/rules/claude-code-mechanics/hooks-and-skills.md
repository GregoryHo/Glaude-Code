# Hooks & Skills Mechanics

## Hook Event Lifecycle

SessionStart → UserPromptSubmit → PreToolUse → (tool) → PostToolUse/PostToolUseFailure → ... → Stop → SessionEnd

Additional events: Notification, SubagentStart, SubagentStop, TeammateIdle, TaskCompleted, PreCompact, PermissionRequest

## Blocking Behavior

**CAN block** (exit code 2 or JSON decision prevents action):
PreToolUse, UserPromptSubmit, Stop, SubagentStop, TeammateIdle, TaskCompleted, PermissionRequest

**CANNOT block** (informational only, action already happened or can't be prevented):
PostToolUse, PostToolUseFailure, Notification, SubagentStart, SessionStart, SessionEnd, PreCompact

## Hook Configuration

- Configured in **settings.json** (not a separate hooks file)
- User: `~/.claude/settings.json` — Project: `.claude/settings.json` — Local: `.claude/settings.local.json` (gitignored)
- WRONG: "hooks go in hooks.json at project root" — they go in settings.json under `hooks` key

## Skills

- Auto-discover from `~/.claude/skills/<name>/SKILL.md` and `.claude/skills/<name>/SKILL.md`
- Recursive directory discovery — nested paths work
- Descriptions always in context; full SKILL.md loads only on invocation
- Frontmatter: `name`, `description`, `allowed-tools`, `model`, `context`, `agent`, `hooks`, `user-invocable`, `disable-model-invocation`, `argument-hint`
- WRONG: "skills must be registered somewhere" — they auto-discover from skills directories
