# MCP (Model Context Protocol) Services

This directory contains MCP server configurations and management tools for Claude Code.

## Quick Start - Selective Installation

```bash
# 1. See what's available (grouped by category)
python3 install_mcp.py list

# 2. Get recommendations for your use case
python3 install_mcp.py recommend starter

# 3. Install only what you need
python3 install_mcp.py install context7

# 4. Check what's installed
python3 install_mcp.py status
```

## Common Installation Examples

```bash
# Install documentation helper (recommended starter)
python3 install_mcp.py install context7

# Install problem-solving assistant
python3 install_mcp.py install sequential-thinking

# Install multiple servers
python3 install_mcp.py install context7 sequential-thinking

# Remove servers you don't need
python3 install_mcp.py remove magic
```

## Available Servers by Category

### 📚 Documentation & Learning
- **context7** ✓ - Official library documentation and code examples

### 🧠 Problem Solving
- **sequential-thinking** ✓ - Multi-step problem solving and analysis

### 🔍 Code Analysis
- **serena** ✓ - Semantic code analysis and intelligent editing

### 🧪 Testing
- **playwright** ✓ - Browser E2E testing and automation

### 🎨 UI Generation
- **magic** 🔑 - Modern UI component generation (needs TWENTYFIRST_API_KEY)

### ✏️ Code Modification
- **morphllm-fast-apply** 🔑 - Context-aware code modifications (needs MORPH_API_KEY)

### 📝 Productivity
- **notion** 🔑 - Official Notion integration (needs NOTION_TOKEN)
- **notion-safe** 🔑 - Notion wrapper with rate limiting and audit logging (needs NOTION_TOKEN)

**Legend:** ✓ = No API key needed, 🔑 = API key required

## Recommended Starting Configurations

### Minimal Setup (No API Keys)
```bash
python3 install_mcp.py install context7
```

### Basic Development
```bash
python3 install_mcp.py install context7 sequential-thinking
```

### Full Stack Development (No API Keys)
```bash
python3 install_mcp.py install context7 serena playwright sequential-thinking
```

## Directory Structure

```
mcp/
├── configs/             # Individual MCP server configurations
│   ├── context7.json
│   ├── sequential.json
│   ├── magic.json
│   ├── playwright.json
│   ├── serena.json
│   ├── morphllm.json
│   ├── notion.json
│   └── notion-safe.json
├── MCP_*.md            # Detailed documentation for each server
├── install_mcp.py      # Installation and management script
└── notion-safe/        # Custom Notion wrapper with rate limiting
```

## Documentation

Each MCP server has detailed documentation in its corresponding `MCP_*.md` file:
- When to use the server
- Comparison with alternatives
- Integration patterns with other servers
- Usage examples and decision logic

## Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Notion integration
export NOTION_TOKEN='your-notion-token'

# Magic UI generation
export TWENTYFIRST_API_KEY='your-21st-key'

# MorphLLM Fast Apply
export MORPH_API_KEY='your-morph-key'
```

## Adding New Servers

1. Edit `mcp-servers.json` to add server configuration
2. Run `python3 install_mcp.py install <server-name>`
3. Restart Claude Code

## Troubleshooting

- **Server not appearing**: Restart Claude Code after installation
- **API errors**: Check environment variables are set correctly
- **Rate limits**: The `notion-safe` wrapper limits to 100 ops/hour automatically (plain `notion` has no limit)

## Backups

The installer automatically creates timestamped backups:
- Location: `~/.claude.json.backup.YYYYMMDD_HHMMSS`
- Restore: `cp ~/.claude.json.backup.* ~/.claude.json`