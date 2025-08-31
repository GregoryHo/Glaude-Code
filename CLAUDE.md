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

### MCP Services Management
```bash
# List all available MCP servers
python3 mcp/install_mcp.py list

# Install all MCP servers to Claude Code
python3 mcp/install_mcp.py install

# Install specific servers
python3 mcp/install_mcp.py install notion serena magic

# Remove servers
python3 mcp/install_mcp.py remove magic

# Check installation status
python3 mcp/install_mcp.py status

# Install Notion MCP dependencies (for wrapper)
cd mcp/notion && npm install

# Test Notion wrapper
cd mcp/notion && npm test
```

### Required Environment Variables
```bash
# For Notion integration
export NOTION_TOKEN='your-token'

# For Magic UI generation
export TWENTYFIRST_API_KEY='your-key'

# For MorphLLM Fast Apply
export MORPH_API_KEY='your-key'
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
├── core/                # Files deployed to ~/.claude/
│   ├── CLAUDE.md        # Global instructions
│   └── settings.json    # Permission & behavior settings
├── mcp/                 # MCP service configurations and wrappers
│   ├── configs/         # Individual JSON config files per server
│   ├── MCP_*.md         # Documentation for each MCP server
│   ├── install_mcp.py   # MCP installation manager
│   └── notion/          # Rate-limited Notion wrapper (100 ops/hour)
├── agents/              # Custom AI agent definitions
├── templates/           # Reusable workflow templates
└── install.sh           # Main deployment script
```

## Working with MCP Services

### Available MCP Servers

#### 🔸 **context7** - Documentation & Examples
- Official library documentation and code examples
- No API key required
- Command: `npx -y @upstash/context7-mcp@latest`

#### 🔸 **sequential-thinking** - Problem Solving
- Multi-step problem solving and systematic analysis
- No API key required
- Command: `npx -y @modelcontextprotocol/server-sequential-thinking`

#### 🔸 **magic** - UI Generation
- Modern UI component generation and design systems
- Requires: `TWENTYFIRST_API_KEY`
- Command: `npx @21st-dev/magic`

#### 🔸 **playwright** - Browser Testing
- Cross-browser E2E testing and automation
- No API key required
- Command: `npx @playwright/mcp@latest`

#### 🔸 **serena** - Code Analysis
- Semantic code analysis and intelligent editing
- No API key required
- Command: `uvx --from git+https://github.com/oraios/serena serena start-mcp-server`

#### 🔸 **morphllm-fast-apply** - Code Modification
- Fast Apply capability for context-aware code modifications
- Requires: `MORPH_API_KEY`
- Command: `npx @morph-llm/morph-fast-apply`

#### 🔸 **notion** - Productivity Integration
- Rate-limited Notion integration (100 ops/hour)
- Requires: `NOTION_TOKEN`
- Custom wrapper with rate limiting and logging

### Notion Wrapper Features
- **Rate Limiting**: 100 operations/hour with automatic queuing
- **Logging**: All operations logged to `mcp/notion/logs/`
- **Error Handling**: Retry logic with exponential backoff
- **Zone Isolation**: Optional workspace filtering

### Adding New MCP Services
1. Add server configuration to `mcp/mcp-servers.json`
2. Optionally create wrapper directory: `mcp/{service-name}/`
3. Add wrapper with rate limiting pattern from Notion example
4. Test thoroughly before deployment using `install_mcp.py`

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