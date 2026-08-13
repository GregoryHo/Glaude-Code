# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Context

This is a **meta-configuration framework** for developing and managing Claude Code tools. It:
- Deploys to `~/.claude/` and affects ALL Claude Code sessions
- Changes here have **global impact** across all projects
- Serves as a **development workspace** for MCP servers, integrations, and agents

**Your Role**: Help develop, test, and maintain this tool library - NOT to use these tools for end-user tasks.

---

## Development Workflow

When working on this project, follow this workflow:

### 1. Understanding the Request
Determine if the request is:
- **Development Task**: Adding/modifying MCP servers, integrations, or framework features
- **Documentation Task**: Updating guides, README files, or configuration docs
- **Testing Task**: Validating MCP servers, testing deployment, or debugging

### 2. Development Process
```bash
# 1. Check current state
git status
python3 mcp/install_mcp.py status

# 2. Make changes in this repository
# - Add MCP configs to mcp/configs/
# - Create wrappers in mcp/{service-name}/
# - Add integrations to integrations/

# 3. Test locally (without deploying)
cd mcp/{service-name} && npm test

# 4. Validate configurations
python3 -m json.tool mcp/configs/{service-name}.json
grep -r "TOKEN|KEY|SECRET" --exclude-dir=node_modules --exclude-dir=.git

# 5. Deploy only when ready
./install.sh
```

### 3. Key Principles
- **Test before deploying** - Changes affect global Claude Code behavior
- **Document everything** - Update README.md and MCP_*.md files
- **Keep it agnostic** - No personal/work-specific data
- **Security first** - Never commit secrets

---

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

**When to Use Wrappers**:
- Rate limiting required (e.g., Notion API has limits)
- Audit logging needed (enterprise/compliance)
- Safety checks for write operations
- Batch processing for large operations

### Deployment Flow
1. Source files in `Glaude-Code/core/`
2. `install.sh` creates timestamped backup of `~/.claude/`
3. Deploys `core/CLAUDE.md` and `core/settings.json` to `~/.claude/`
4. Active in all new Claude Code sessions

---

## Directory Structure

```
.
├── core/                # Files deployed to ~/.claude/
│   ├── CLAUDE.md        # Global instructions (this gets deployed)
│   └── settings.json    # Permission & behavior settings
├── mcp/                 # MCP service configurations and wrappers
│   ├── configs/         # Individual JSON config files per server
│   ├── MCP_*.md         # Documentation for each MCP server
│   ├── install_mcp.py   # MCP installation manager
│   └── {service}/       # Custom wrappers (e.g., notion-safe/)
├── integrations/        # Non-MCP third-party integrations
│   ├── obsidian/        # File-based knowledge management
│   └── excalidraw/      # Diagram generation
├── agents/              # Custom AI agent definitions
├── templates/           # Reusable workflow templates
├── install.sh           # Main deployment script
└── README.md            # User-facing documentation
```

### Responsibility Separation
- **CLAUDE.md** (this file) → Development guidance for AI
- **README.md** → End-user installation and usage guide
- **mcp/README.md** → MCP services usage documentation
- **integrations/README.md** → Third-party integrations guide
- **mcp/MCP_*.md** → Individual service documentation

---

## Understanding MCP Wrappers

### When to Create a Wrapper
Create a custom wrapper when:
1. **Rate Limiting**: API has strict rate limits (e.g., Notion: 3 req/sec)
2. **Audit Logging**: Need to track all operations for compliance
3. **Safety Checks**: Prevent destructive operations in production
4. **Batch Processing**: Split large operations automatically
5. **State Management**: Need to maintain session state between calls

### Wrapper Architecture
```javascript
// mcp/{service}/src/{service}-wrapper.js
const { spawn } = require('child_process');

// 1. Rate limiter
const rateLimiter = new RateLimiter({
  maxOps: 100,
  windowMs: 3600000
});

// 2. Logger
const logger = createLogger({
  logDir: '~/.{service}-logs',
  format: 'jsonl'
});

// 3. Safety validator
function validateOperation(operation, args) {
  if (operation.type === 'delete') {
    return { safe: false, reason: 'Destructive operation' };
  }
  return { safe: true };
}

// 4. Spawn official MCP server
const mcp = spawn('npx', ['@official/mcp-server']);

// 5. Intercept and wrap requests
mcp.stdin.write(JSON.stringify(wrappedRequest));
```

### Example: notion-safe Wrapper
See `mcp/notion-safe/` for a complete implementation with:
- Rate limiting (100 ops/hour)
- JSONL audit logs
- Batch processing for large writes
- Pre-execution safety checks

---

## Adding New MCP Services

### Step-by-Step Guide

#### 1. Create Configuration File
```bash
# Create config file
cat > mcp/configs/{service-name}.json << 'EOF'
{
  "mcpServers": {
    "service-name": {
      "command": "npx",
      "args": ["@org/package@latest"],
      "env": {
        "API_KEY": "${SERVICE_API_KEY}"
      }
    }
  }
}
EOF
```

#### 2. Update install_mcp.py Metadata
```python
# Add to SERVER_METADATA in mcp/install_mcp.py
"service-name": {
    "requires_api_key": True,
    "api_key_env": "SERVICE_API_KEY",
    "category": "category-name",
    "description": "Service description"
}
```

#### 3. Create Wrapper (Optional)
Only if rate limiting or logging is needed:
```bash
mkdir -p mcp/{service-name}/src
cp mcp/notion-safe/src/notion-mcp-wrapper.js mcp/{service-name}/src/{service}-wrapper.js
# Modify wrapper for specific service
```

#### 4. Test the Service
```bash
# Test configuration validity
python3 -m json.tool mcp/configs/{service-name}.json

# Install to Claude Code
python3 mcp/install_mcp.py install {service-name}

# Verify in config
cat ~/.claude.json | jq '.mcpServers."{service-name}"'

# Test with environment variable
export SERVICE_API_KEY='test-key'
npx @org/package@latest
```

#### 5. Document the Service
Create `mcp/MCP_{ServiceName}.md`:
```markdown
# {Service Name} MCP Server

## Overview
Brief description of what this service does.

## Installation
\`\`\`bash
python3 mcp/install_mcp.py install {service-name}
\`\`\`

## Configuration
Required environment variables: SERVICE_API_KEY

## Usage Examples
How to use this service in Claude Code.

## When to Use
- Use case 1
- Use case 2

## Comparison with Alternatives
How this compares to similar services.
```

---

## Adding Third-Party Integrations

For tools that don't have MCP servers, create file-based integrations.

### Integration Structure
```
integrations/{tool}/
├── README.md           # Usage documentation
├── scripts/            # Helper scripts
├── templates/          # Reusable templates
└── examples/           # Example usage
```

### Example: Obsidian Integration
Uses direct file access instead of MCP:
```bash
# Read notes
Grep "TODO" --path ${OBSIDIAN_VAULT_PATH}

# Open notes via URI scheme
open "obsidian://open?vault=${VAULT_NAME}&file=note.md"
```

### Example: Excalidraw Integration
Uses JSON generation:
```bash
# Convert Mermaid diagrams
node integrations/excalidraw/mermaid-to-excalidraw.js input.mmd output.excalidraw

# Use templates
cp integrations/excalidraw/templates/architecture.json my-diagram.excalidraw
```

See `integrations/README.md` for full integration guide.

---

## Common Development Tasks

### Debugging MCP Services

```bash
# Check if MCP server is properly configured
cat ~/.claude.json | jq '.mcpServers'

# Test MCP server directly (bypass Claude Code)
export NOTION_TOKEN='your-token'
npx @notionhq/notion-mcp-server

# Check wrapper logs (if using wrapper)
tail -f ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl

# Debug environment variables (safely)
env | grep -E "_TOKEN|_KEY" | sed 's/=.*/=***/'
```

### Troubleshooting

#### MCP Server Not Working
1. Check if server is installed: `python3 mcp/install_mcp.py status`
2. Verify environment variables are set correctly
3. Restart Claude Code after installation
4. Check `~/.claude.json` for proper configuration
5. Test server directly outside of Claude Code

#### Wrapper Issues
- Check wrapper logs for errors
- Verify rate limits aren't exceeded
- Ensure wrapper dependencies are installed (`npm install`)
- Test official MCP server first (bypass wrapper)

#### Installation Failures
- Restore from backup: `cp -r ~/.claude.backup.{timestamp}/* ~/.claude/`
- Check Python version: `python3 --version` (requires 3.6+)
- Verify npm is installed: `npm --version`
- Check permissions on `~/.claude/` directory

---

## Testing Procedures

### Before Deployment Checklist
- [ ] Test MCP services locally: `cd mcp/{service} && npm test`
- [ ] Validate all JSON configs: `python3 -m json.tool core/settings.json`
- [ ] Check for exposed secrets: `grep -r "TOKEN|KEY|SECRET" --exclude-dir=node_modules --exclude-dir=.git`
- [ ] Test install_mcp.py changes: `python3 mcp/install_mcp.py list`
- [ ] Verify documentation is updated

### Rollback Procedure
```bash
# List available backups
ls -la ~/.claude.backup.*

# Restore from specific backup
cp -r ~/.claude.backup.20241023_143022/* ~/.claude/

# Restart Claude Code to apply
```

### Testing New Features
```bash
# 1. Test in isolation (don't deploy)
cd mcp/{service-name}
npm test

# 2. Test with real MCP server
export SERVICE_API_KEY='test-key'
npx @org/package@latest

# 3. Test installation script
python3 mcp/install_mcp.py install {service-name} --dry-run

# 4. Deploy to test environment first
./install.sh
# Test in Claude Code with non-critical project

# 5. If successful, deploy to production
git commit -m "Add {service-name} MCP server"
git push
```

---

## Critical Warnings

### ⚠️ NEVER
- Commit API keys, tokens, or secrets to this repository
- Make breaking changes without backward compatibility
- Deploy untested MCP services to production
- Include personal/work-specific data in this framework
- Modify `~/.claude/` directly (always use `install.sh` for backups)
- Push changes without running security checks

### ✅ ALWAYS
- Test changes locally before deployment
- Create timestamped backups (automatic with `install.sh`)
- Keep framework project-agnostic (works for anyone)
- Document all configuration changes
- Run `grep -r "TOKEN|KEY|SECRET"` before commits
- Update README.md when adding new features
- Verify JSON syntax before committing

### Security Checklist Before Commit
```bash
# 1. Check for secrets
grep -r "TOKEN|KEY|SECRET" --exclude-dir=node_modules --exclude-dir=.git

# 2. Validate environment variable usage
grep -r "export.*=.*['\"]" --exclude-dir=node_modules

# 3. Check for hardcoded paths
grep -r "/Users/" --exclude-dir=node_modules --exclude=CLAUDE.md

# 4. Verify .gitignore coverage
git status --ignored

# 5. Review staged changes
git diff --staged
```

---

## Important Notes

### Framework Dependencies
- This framework is referenced by other projects (e.g., `~/Workspace/Personal`)
- Path changes require updates in all dependent projects
- Document any path changes in git commit messages

### Technical Requirements
- MCP services run with Node.js CommonJS modules
- `settings.json` controls tool permissions globally
- All MCP servers are optional - core functionality works without them
- Restart Claude Code after installing/removing MCP servers

### Maintenance Guidelines
- Review and update MCP server versions quarterly
- Check for deprecated APIs in official MCP servers
- Monitor rate limits and adjust wrappers as needed
- Keep documentation in sync with code changes

### User Guidance
For end-users wanting to use this framework, direct them to:
- **README.md** - Installation and quick start
- **mcp/README.md** - MCP services usage guide
- **integrations/README.md** - Third-party integrations
- **mcp/MCP_*.md** - Specific service documentation
