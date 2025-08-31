# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Context

This is a **meta-configuration framework** that deploys to `~/.claude/` and affects ALL Claude Code sessions. Changes here have global impact.

## Common Commands

### Installation & Deployment
```bash
# Full installation (backs up existing config)
./install.sh

# Manual deployment (selective)
cp core/CLAUDE.md ~/.claude/
cp core/settings.json ~/.claude/
```

### MCP Services
```bash
# Install Notion MCP dependencies
cd mcp/notion && npm install

# Test Notion wrapper
cd mcp/notion && npm test

# Run Notion wrapper (requires NOTION_TOKEN env)
export NOTION_TOKEN='your-token'
node mcp/notion/src/notion-mcp-wrapper.js
```

## Architecture

### Configuration Hierarchy
1. **Global Level**: `~/.claude/CLAUDE.md` - Applies to all projects
2. **Project Level**: `{project}/CLAUDE.md` - Project-specific overrides
3. **Session Context**: Runtime configurations and MCP states

### MCP Wrapper Pattern
```
Claude Code
    ↓
Wrapper Layer (rate limiting, logging, isolation)
    ↓
Official MCP Server
    ↓
External API
```

### Deployment Flow
1. Source files in `Glaude-Code/core/`
2. `install.sh` creates timestamped backup
3. Deploys to `~/.claude/`
4. Active in all new Claude Code sessions

## Directory Structure

```
.
├── core/           # Files deployed to ~/.claude/
│   ├── CLAUDE.md   # Global instructions
│   └── settings.json # Permission & behavior settings
├── mcp/            # MCP service wrappers
│   └── notion/     # Rate-limited Notion wrapper (100 ops/hour)
├── agents/         # Custom AI agent definitions
├── templates/      # Reusable workflow templates
└── install.sh      # Deployment script
```

## Working with MCP Services

### Notion Wrapper Features
- **Rate Limiting**: 100 operations/hour with automatic queuing
- **Logging**: All operations logged to `mcp/notion/logs/`
- **Error Handling**: Retry logic with exponential backoff
- **Zone Isolation**: Optional workspace filtering

### Adding New MCP Services
1. Create directory: `mcp/{service-name}/`
2. Add wrapper with rate limiting pattern from Notion example
3. Update `install.sh` to reference new service
4. Test thoroughly before deployment

## Testing Procedures

### Before Deployment Checklist
- [ ] Test MCP services: `cd mcp/{service} && npm test`
- [ ] Validate JSON configs: `python3 -m json.tool core/settings.json`
- [ ] Check for API keys in code: `grep -r "TOKEN\|KEY\|SECRET" --exclude-dir=node_modules`
- [ ] Run install script in dry-run mode (if implementing)

### Rollback Procedure
```bash
# Backups are created automatically with timestamp
ls -la ~/.claude.backup.*
# Restore from backup
cp -r ~/.claude.backup.{timestamp}/* ~/.claude/
```

## Critical Warnings

⚠️ **NEVER**:
- Commit API keys, tokens, or secrets
- Make breaking changes without backward compatibility
- Deploy untested MCP services
- Include personal/work-specific data in this framework

✅ **ALWAYS**:
- Test changes locally before deployment
- Create timestamped backups
- Keep framework project-agnostic
- Document all configuration changes

## Important Notes

- Framework is referenced by other projects (e.g., `~/Workspace/Personal`)
- Path changes require updates in all dependent projects
- MCP services run with Node.js CommonJS modules
- Settings.json controls tool permissions globally