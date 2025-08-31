# Glaude-Code Configuration Framework

A personalized Claude Code configuration framework for enhanced productivity and workflow optimization.

## 🎯 Purpose

This framework provides a structured approach to:
- Configure and manage MCP (Model Context Protocol) servers
- Define personalized AI agents for specific tasks
- Maintain consistent development practices across projects
- Create reusable templates for common workflows

## 📁 Structure

```
Glaude-Code/
├── core/                 # Core configuration files
│   ├── CLAUDE.md        # Global Claude instructions
│   └── settings.json    # Claude settings
├── mcp/                 # MCP service configurations
│   └── notion/          # Notion API wrapper with rate limiting
├── agents/              # Custom AI agents
│   ├── management/      # Management-focused agents
│   └── technical/       # Technical-focused agents
├── templates/           # Reusable templates
│   ├── prd/            # Product requirement documents
│   ├── architecture/   # Architecture decision records
│   └── review/         # Performance review templates
└── docs/               # Documentation
```

## 🚀 Quick Start

### Installation

1. Clone this repository:
```bash
git clone ~/GitHub/AI/Glaude-Code
cd ~/GitHub/AI/Glaude-Code
```

2. Run the installation script:
```bash
./install.sh
```

This will:
- Deploy core configurations to `~/.claude/`
- Set up MCP servers
- Configure custom agents

### Manual Setup

If you prefer manual setup:

1. Copy core files:
```bash
cp core/CLAUDE.md ~/.claude/
cp core/settings.json ~/.claude/
```

2. Configure MCP servers as needed (see `mcp/` directory)

## 🔧 MCP Services

### Notion Integration

The framework includes a production-ready Notion MCP wrapper with:
- Rate limiting (100 operations/hour)
- Comprehensive logging
- Error handling
- Zone isolation support

Setup:
```bash
cd mcp/notion
npm install
./scripts/setup-wrapper.sh
```

## 📚 Templates

Pre-configured templates for common tasks:
- Product Requirements Documents (PRD)
- Architecture Decision Records (ADR)
- Performance Reviews
- Sprint Planning

## 🤝 Contributing

This is a personal configuration framework, but feel free to fork and adapt for your needs.

## 📝 License

MIT License - See LICENSE file for details
