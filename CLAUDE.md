# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Context

This is a **meta-configuration framework** that deploys to `~/.claude/` and affects ALL Claude Code sessions. Changes here have global impact.

## Quick Reference

### Most Used Commands
```bash
# Deploy framework
./install.sh

# MCP server management
python3 mcp/install_mcp.py list                    # List available servers
python3 mcp/install_mcp.py install context7        # Install specific server
python3 mcp/install_mcp.py status                  # Check installation status

# Test Notion wrapper
cd mcp/notion && npm test

# Check for secrets before commit
grep -r "TOKEN\|KEY\|SECRET" --exclude-dir=node_modules
```

### 🏭 Agent Factory - Pydantic AI Agent Builder
```bash
# To build AI agents using the Agent Factory framework:
cd ~/GitHub/AI/context-engineering-intro/use-cases/agent-factory-with-subagents

# Then open Claude Code in that directory and use trigger phrases:
# - "Build an AI agent that..."
# - "Create a Pydantic AI agent for..."
# - "I need an AI assistant that can..."

# Quick access via symlink (if created):
cd ~/GitHub/AI/Glaude-Code/agents/agent-factory
```

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

### Testing Commands
```bash
# Test Notion wrapper functionality
cd mcp/notion && npm test

# Validate all JSON configurations
python3 -m json.tool core/settings.json
for file in mcp/configs/*.json; do python3 -m json.tool "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"; done

# Test MCP server installation (dry run)
python3 mcp/install_mcp.py status

# Verify Notion wrapper setup
cd mcp/notion && npm run test:setup

# Check for exposed secrets
grep -r "TOKEN\|KEY\|SECRET" --exclude-dir=node_modules --exclude-dir=.git

# Validate environment variables
env | grep -E "NOTION_TOKEN|TWENTYFIRST_API_KEY|MORPH_API_KEY|CONTEXT7_API_KEY" | sed 's/=.*/=***/'
```

### Required Environment Variables
```bash
# For Notion integration
export NOTION_TOKEN='your-token'

# For Magic UI generation
export TWENTYFIRST_API_KEY='your-key'

# For MorphLLM Fast Apply
export MORPH_API_KEY='your-key'

# For Context7 (optional, for higher rate limits)
export CONTEXT7_API_KEY='your-key'
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

#### Step-by-Step Guide
1. **Create configuration file**: `mcp/configs/{service-name}.json`
   ```json
   {
     "service-name": {
       "command": "npx",
       "args": ["@org/package@latest"],
       "env": {}
     }
   }
   ```

2. **Add metadata** to `install_mcp.py`:
   ```python
   "service-name": {
       "requires_api_key": True/False,
       "api_key_env": "SERVICE_API_KEY",
       "category": "category-name",
       "description": "Service description"
   }
   ```

3. **Create wrapper (if rate limiting needed)**:
   ```bash
   mkdir -p mcp/{service-name}/src
   cp mcp/notion/src/notion-mcp-wrapper.js mcp/{service-name}/src/{service}-wrapper.js
   # Modify wrapper for specific service
   ```

4. **Test the service**:
   ```bash
   # Install to Claude Code
   python3 mcp/install_mcp.py install {service-name}
   
   # Verify in config
   cat ~/.claude.json | jq '.mcpServers.{service-name}'
   
   # Test with environment variable
   export SERVICE_API_KEY='test-key'
   npx @org/package@latest
   ```

5. **Document the service**: Create `mcp/MCP_{ServiceName}.md`

## Common Development Tasks

### Debugging MCP Services
```bash
# Check if MCP server is properly configured
cat ~/.claude.json | jq '.mcpServers'

# Test MCP server directly
export NOTION_TOKEN='your-token'
npx @notionhq/notion-mcp-server

# Check logs for wrapper services
tail -f mcp/notion/logs/notion-mcp-*.log

# Debug environment variables
env | grep -E "_TOKEN|_KEY" | sed 's/=.*/=***/'
```

### Troubleshooting

#### MCP Server Not Working
1. Check if server is installed: `python3 mcp/install_mcp.py status`
2. Verify environment variables are set
3. Restart Claude Code after installation
4. Check ~/.claude.json for proper configuration

#### Notion Rate Limiting Issues
- Wrapper enforces 100 ops/hour
- Check logs: `tail -f mcp/notion/logs/notion-mcp-*.log`
- Queue status visible in logs

#### Installation Failures
- Restore from backup: `cp -r ~/.claude.backup.{timestamp}/* ~/.claude/`
- Check Python version: `python3 --version` (requires 3.6+)
- Verify npm is installed: `npm --version`

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
- Modify ~/.claude/ directly without using install.sh (creates backups)

✅ **ALWAYS**:
- Test changes locally before deployment
- Create timestamped backups
- Keep framework project-agnostic
- Document all configuration changes
- Run `grep -r "TOKEN\|KEY\|SECRET"` before commits

## Important Notes

- Framework is referenced by other projects (e.g., `~/Workspace/Personal`)
- Path changes require updates in all dependent projects
- MCP services run with Node.js CommonJS modules
- Settings.json controls tool permissions globally
- All MCP servers are optional - core functionality works without them
- Restart Claude Code after installing/removing MCP servers