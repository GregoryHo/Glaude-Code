# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Critical Context

This repository holds a personal `~/.claude/` configuration, kept public
so it can be reused. It:
- Deploys to `~/.claude/` via `install.sh` and affects ALL Claude Code sessions
- Is normally edited the other way round: change `~/.claude/` first, then
  pull the change back into `core/`
- Serves as a **development workspace** for MCP servers, integrations, and agents

**Your Role**: Maintain this configuration and its tooling. Opinionated
defaults are fine; machine-specific ones are not.

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
- **Stay portable** - Opinionated defaults belong here; secrets, machine paths,
  and work-specific data do not (see Portability Test)
- **Security first** - Never commit secrets

---

## Understanding MCP Wrappers

```
Claude Code
    ↓
Wrapper Layer (rate limiting, logging, isolation)
    ↓
Official MCP Server
    ↓
External API
```

### When to Create a Wrapper
Create a custom wrapper when:
1. **Rate Limiting**: API has strict rate limits (e.g., Notion: 3 req/sec)
2. **Audit Logging**: Need to track all operations for compliance
3. **Safety Checks**: Prevent destructive operations in production
4. **Batch Processing**: Split large operations automatically
5. **State Management**: Need to maintain session state between calls

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

Paths that point back into this repository must use the `${GLAUDE_ROOT}`
placeholder, which `install_mcp.py` expands to the checkout location. Never
hardcode an absolute path.

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

## Critical Warnings

### Portability Test
This repository is public. Before committing, sort the change into one of three tiers:

1. **Breaks or leaks for other people** - secrets, absolute machine paths,
   work-specific data. Never commit these.
2. **Opinionated but harmless** - editor mode, theme, output style, plugin list,
   hooks. Commit freely, but `install.sh` must never force them onto anyone.
3. **Opinionated and the whole point** - permission deny lists, the MCP wrapper
   pattern, `core/rules/`. This is what the repository exists to share.

Only tier 1 is banned. Being opinionated is not a defect — neutrality belongs in
the deployment mechanism, not in the content.

### ⚠️ NEVER
- Commit API keys, tokens, or secrets to this repository
- Commit absolute machine paths or work-specific data (tier 1 above)
- Make breaking changes without backward compatibility
- Deploy untested MCP services to production
- Let `core/` drift from `~/.claude/` — sync changes back after editing the live config
- Push changes without running security checks

### ✅ ALWAYS
- Test changes locally before deployment
- Keep `core/` in sync with `~/.claude/` (edit the live config first, then pull it back)
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

### Documentation Map
- **CLAUDE.md** (this file) - Guidance for Claude Code working in this repository
- **README.md** - Installation and quick start
- **mcp/README.md** - MCP services usage guide
- **integrations/README.md** - Third-party integrations guide
- **mcp/MCP_*.md** - Individual service documentation
