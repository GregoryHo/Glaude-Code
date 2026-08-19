# Third-Party Integrations

Non-MCP integrations for external tools and services.

## Overview

This directory contains integrations that don't use the Model Context Protocol (MCP). These are file-based, URI-based, or tool-based integrations that leverage Claude Code's native capabilities or external utilities.

## Available Integrations

### 📝 [Obsidian](./obsidian/)
Knowledge base integration via direct file system access and Obsidian URI scheme.

**Features**:
- Read and search existing notes
- Batch create/modify notes
- Open specific notes in Obsidian
- No MCP server required

**Use Cases**: Note-taking, knowledge management, documentation

---

### 🎨 [Excalidraw](./excalidraw/)
Hand-drawn diagram generation with two approaches:
1. Mermaid → Excalidraw (official tool)
2. Direct JSON generation (full control)

**Features**:
- Generate flowcharts, architecture diagrams, mind maps, UML
- Hand-drawn style rendering
- Templates for common diagram types
- No MCP server required

**Use Cases**: System design, documentation, visual thinking

---

## Why Not MCP?

These integrations don't use MCP because:
- **Obsidian**: Direct file access is simpler and more reliable than community MCP servers
- **Excalidraw**: Official conversion tools and JSON format provide sufficient functionality

## External Integration

These tools are designed to be reusable. Other projects can:
1. Copy the integration directory
2. Follow the README in each integration
3. Adapt to their specific needs

## Directory Structure

```
integrations/
├── README.md              # This file
├── obsidian/              # Obsidian integration
│   ├── README.md
│   └── WORKFLOWS.md
└── excalidraw/            # Excalidraw integration
    ├── README.md
    ├── mermaid-to-excalidraw.js
    ├── package.json
    └── templates/
```

## Contributing

To add a new integration:
1. Create a new directory under `integrations/`
2. Add a comprehensive README.md
3. Include usage examples
4. Update this README

## See Also

- [MCP Servers](../mcp/) - Model Context Protocol integrations
- [Core Configuration](../core/) - Global Claude Code settings
