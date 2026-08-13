# Glaude-Code Configuration Framework

A personalized Claude Code configuration framework for enhanced productivity and workflow optimization.

## 🎯 Purpose

This framework provides a structured approach to:
- Configure and manage MCP (Model Context Protocol) servers
- Define personalized AI agents for specific tasks
- Maintain consistent development practices across projects
- Create reusable templates for common workflows
- Integrate third-party tools (Obsidian, Excalidraw, etc.)

---

## 📁 Structure

```
Glaude-Code/
├── core/                 # Core configuration files
│   ├── CLAUDE.md        # Global Claude instructions
│   └── settings.json    # Claude settings
├── mcp/                 # MCP service configurations
│   ├── configs/         # Individual JSON config files
│   ├── MCP_*.md         # Documentation for each service
│   └── install_mcp.py   # Installation manager
├── integrations/        # Third-party integrations
│   ├── obsidian/        # Obsidian knowledge management
│   └── excalidraw/      # Diagram generation
├── agents/              # Custom AI agents
├── templates/           # Reusable templates
└── install.sh           # Main deployment script
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/Glaude-Code.git
cd Glaude-Code

# Run the installation script
./install.sh
```

This will:
- Create timestamped backup of existing `~/.claude/` configuration
- Deploy `core/CLAUDE.md` and `core/settings.json` to `~/.claude/`
- Make configurations active for all Claude Code sessions

### 2. Install MCP Services

```bash
# See available MCP servers
python3 mcp/install_mcp.py list

# Install recommended starter pack (no API keys needed)
python3 mcp/install_mcp.py install context7

# Install multiple services
python3 mcp/install_mcp.py install context7 playwright sequential-thinking

# Check installation status
python3 mcp/install_mcp.py status
```

### 3. Configure Environment Variables

For MCP services that require API keys, add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Notion integration (optional)
export NOTION_TOKEN='your-notion-token'

# Magic UI generation (optional)
export TWENTYFIRST_API_KEY='your-21st-key'

# MorphLLM Fast Apply (optional)
export MORPH_API_KEY='your-morph-key'

# Context7 (optional, for higher rate limits)
export CONTEXT7_API_KEY='your-key'
```

Then reload your shell: `source ~/.zshrc`

---

## 🛠️ MCP Services

### Available Services

| Service | Category | API Key | Description |
|---------|----------|---------|-------------|
| **context7** | Documentation | Optional | Official library documentation and code examples |
| **sequential-thinking** | Problem Solving | No | Multi-step problem solving and analysis |
| **serena** | Code Analysis | No | Semantic code analysis and intelligent editing |
| **playwright** | Testing | No | Cross-browser E2E testing and automation |
| **selenium** | Testing | No | Industry-standard browser automation |
| **chrome-devtools** | Browser | No | Chrome DevTools Protocol for debugging |
| **archon** | Knowledge | No | AI-powered knowledge base and task management |
| **magic** | UI Generation | Yes | Modern UI component generation |
| **morphllm-fast-apply** | Code Modification | Yes | Context-aware code modifications |
| **notion** | Productivity | Yes | Official Notion integration |
| **notion-safe** | Productivity | Yes | Enterprise Notion wrapper with safety features |

### Quick Commands

```bash
# List all available MCP servers
python3 mcp/install_mcp.py list

# Get recommendations for your use case
python3 mcp/install_mcp.py recommend starter

# Install specific server
python3 mcp/install_mcp.py install context7

# Install multiple servers
python3 mcp/install_mcp.py install notion serena magic

# Remove server
python3 mcp/install_mcp.py remove magic

# Check what's installed
python3 mcp/install_mcp.py status
```

### Recommended Configurations

**Minimal Setup** (No API keys):
```bash
python3 mcp/install_mcp.py install context7
```

**Basic Development**:
```bash
python3 mcp/install_mcp.py install context7 sequential-thinking
```

**Full Stack Development**:
```bash
python3 mcp/install_mcp.py install context7 serena playwright sequential-thinking
```

**With Task Management**:
```bash
python3 mcp/install_mcp.py install context7 archon notion
```

---

## 🧪 Browser Testing

### Using Playwright (Recommended)

```bash
# Install Playwright MCP
python3 mcp/install_mcp.py install playwright

# Install browser drivers
npx playwright install

# Use in Claude Code with phrases like:
# - "test the login flow"
# - "check if form validation works"
# - "take screenshots of responsive design"
# - "test across Chrome, Firefox, and Safari"
```

### Using Selenium (Legacy)

```bash
# Install Selenium MCP
python3 mcp/install_mcp.py install selenium

# Install browser drivers
npm install -g chromedriver

# Use in Claude Code with phrases like:
# - "test with Selenium WebDriver"
# - "run tests on Selenium Grid"
```

### Using Chrome DevTools

```bash
# Install Chrome DevTools MCP (requires Node.js 22+)
python3 mcp/install_mcp.py install chrome-devtools

# Use for performance analysis and debugging
```

**Choosing the Right Tool**:
- **Playwright**: Modern apps, cross-browser testing, auto-wait features
- **Selenium**: Legacy systems, enterprise environments, WebDriver compliance
- **Chrome DevTools**: Performance profiling, network analysis, debugging

---

## 🔗 Third-Party Integrations

### Obsidian (File-Based Knowledge Management)

```bash
# Set environment variables
export OBSIDIAN_VAULT_PATH="/path/to/vault"
export OBSIDIAN_VAULT_NAME="MyVault"

# Search notes
grep "TODO" --path ${OBSIDIAN_VAULT_PATH}

# Open note in Obsidian
open "obsidian://open?vault=${OBSIDIAN_VAULT_NAME}&file=note.md"
```

See [integrations/obsidian/README.md](integrations/obsidian/README.md) for details.

### Excalidraw (Diagram Generation)

```bash
# Install dependencies
cd integrations/excalidraw
npm install

# Convert Mermaid to Excalidraw
node mermaid-to-excalidraw.js flowchart.mmd flowchart.excalidraw

# Use templates
cp templates/architecture.json my-diagram.excalidraw
```

See [integrations/excalidraw/README.md](integrations/excalidraw/README.md) for details.

---

## 📚 Templates

Pre-configured templates for common tasks:
- **PRD**: Product Requirements Documents
- **ADR**: Architecture Decision Records
- **Reviews**: Performance review templates
- **Sprint Planning**: Sprint planning documents

Located in `templates/` directory.

---

## 🔍 Common Tasks

### Testing MCP Services

```bash
# Test Notion Safe wrapper (if installed)
cd mcp/notion-safe && npm test

# Validate all JSON configurations
python3 -m json.tool core/settings.json
for file in mcp/configs/*.json; do python3 -m json.tool "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"; done

# Check for exposed secrets
grep -r "TOKEN|KEY|SECRET" --exclude-dir=node_modules --exclude-dir=.git

# Verify environment variables
env | grep -E "NOTION_TOKEN|TWENTYFIRST_API_KEY|MORPH_API_KEY|CONTEXT7_API_KEY" | sed 's/=.*/=***/'
```

### Updating the Framework

```bash
# Pull latest changes
git pull origin main

# Re-deploy to ~/.claude/
./install.sh

# Restart Claude Code for changes to take effect
```

### Rolling Back

```bash
# List available backups
ls -la ~/.claude.backup.*

# Restore from backup
cp -r ~/.claude.backup.20241023_143022/* ~/.claude/

# Restart Claude Code
```

---

## 🐛 Troubleshooting

### MCP Server Not Working

1. Check if server is installed:
   ```bash
   python3 mcp/install_mcp.py status
   ```

2. Verify environment variables:
   ```bash
   env | grep -E "_TOKEN|_KEY" | sed 's/=.*/=***/'
   ```

3. Restart Claude Code after installation

4. Check configuration:
   ```bash
   cat ~/.claude.json | jq '.mcpServers'
   ```

### Notion Safe Rate Limiting

If using `notion-safe` wrapper:
- Default limit: 100 operations/hour
- Check logs: `tail -f ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl`
- Increase limit: `export MAX_OPERATIONS_PER_HOUR=200`

### Installation Failures

- Restore from backup: `cp -r ~/.claude.backup.{timestamp}/* ~/.claude/`
- Check Python version: `python3 --version` (requires 3.6+)
- Verify npm is installed: `npm --version`

---

## 📖 Documentation

- **[mcp/README.md](mcp/README.md)** - MCP services usage guide
- **[mcp/MCP_*.md](mcp/)** - Individual service documentation
- **[integrations/README.md](integrations/README.md)** - Third-party integrations
- **CLAUDE.md** - Development guidance (for contributing)

---

## 🔒 Security Best Practices

### Before Committing

```bash
# Check for secrets
grep -r "TOKEN|KEY|SECRET" --exclude-dir=node_modules --exclude-dir=.git

# Check for hardcoded paths
grep -r "/Users/" --exclude-dir=node_modules --exclude=CLAUDE.md

# Review staged changes
git diff --staged
```

### Environment Variables

- Never commit API keys or tokens
- Use environment variables for sensitive data
- Keep `.env` files out of version control
- Use different keys for development/production

---

## 🤝 Contributing

This is a personal configuration framework, but contributions are welcome!

### For Users
- Report issues via GitHub Issues
- Share your MCP server configurations
- Contribute integration guides

### For Developers
See **CLAUDE.md** for development guidance and architectural details.

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🔗 Related Projects

- [Claude Code](https://claude.ai/code) - Official Claude Code interface
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- [Agent Factory](research/agent-factory/) - Pydantic AI agent builder framework

---

## 📞 Support

- **Documentation**: See `mcp/README.md` and `integrations/README.md`
- **Issues**: [GitHub Issues](https://github.com/yourusername/Glaude-Code/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Glaude-Code/discussions)
