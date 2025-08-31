#!/bin/bash

# Glaude-Code Installation Script
# This script deploys the configuration framework to ~/.claude/

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Installing Glaude-Code Configuration Framework${NC}"
echo "================================================"

# Check if running from correct directory
if [ ! -f "README.md" ] || [ ! -d "core" ]; then
    echo -e "${RED}Error: Please run this script from the Glaude-Code directory${NC}"
    exit 1
fi

# Create backup of existing configuration
if [ -d ~/.claude ]; then
    BACKUP_DIR=~/.claude.backup.$(date +%Y%m%d_%H%M%S)
    echo -e "${YELLOW}📦 Backing up existing configuration to $BACKUP_DIR${NC}"
    cp -r ~/.claude "$BACKUP_DIR"
else
    echo -e "${YELLOW}📁 Creating ~/.claude directory${NC}"
    mkdir -p ~/.claude
fi

# Deploy core configuration files
echo -e "${GREEN}📄 Deploying core configuration files...${NC}"

# Copy CLAUDE.md if it exists
if [ -f "core/CLAUDE.md" ]; then
    cp core/CLAUDE.md ~/.claude/
    echo "   ✓ CLAUDE.md deployed"
fi

# Copy settings.json if it exists
if [ -f "core/settings.json" ]; then
    cp core/settings.json ~/.claude/
    echo "   ✓ settings.json deployed"
fi

# Copy personal-context.md if it exists
if [ -f "core/personal-context.md" ]; then
    cp core/personal-context.md ~/.claude/
    echo "   ✓ personal-context.md deployed"
fi

# Deploy agents if directory exists
if [ -d "agents" ] && [ "$(ls -A agents)" ]; then
    echo -e "${GREEN}🤖 Deploying custom agents...${NC}"
    mkdir -p ~/.claude/agents
    cp -r agents/* ~/.claude/agents/
    echo "   ✓ Agents deployed"
fi

# Create MCP configuration
echo -e "${GREEN}⚙️  Configuring MCP services...${NC}"

# Create a reference to Glaude-Code MCP services
cat > ~/.claude/mcp-config.json << EOF
{
  "comment": "MCP services configuration",
  "services": {
    "notion-safe": {
      "description": "Notion API with rate limiting",
      "path": "$(pwd)/mcp/notion/src/notion-mcp-wrapper.js"
    }
  },
  "global_mcps": [
    "filesystem",
    "git",
    "github",
    "memory",
    "brave-search"
  ]
}
EOF
echo "   ✓ MCP configuration created"

# Check if user wants to install MCP servers
echo ""
echo -e "${YELLOW}📋 MCP Server Configuration${NC}"
echo -e "MCP servers extend Claude Code with additional capabilities."
echo ""
echo -e "${YELLOW}Would you like to configure MCP servers? (y/n)${NC}"
read -r INSTALL_MCP

if [[ "$INSTALL_MCP" =~ ^[Yy]$ ]]; then
    # Check if Python is available
    if command -v python3 &> /dev/null; then
        # Make installer executable
        chmod +x mcp/install_mcp.py
        
        echo ""
        echo -e "${GREEN}Available MCP Servers:${NC}"
        echo "  • context7            - Documentation & code examples (recommended)"
        echo "  • sequential-thinking - Multi-step problem solving"
        echo "  • playwright          - Browser testing automation"
        echo "  • serena              - Semantic code analysis"
        echo "  • magic               - UI generation (requires API key)"
        echo "  • morphllm-fast-apply - Code modifications (requires API key)"
        echo "  • notion              - Notion integration (requires API key)"
        
        echo ""
        echo -e "${YELLOW}Enter server names to install (space-separated), or press Enter to skip:${NC}"
        echo -e "${GREEN}Example: context7 sequential-thinking${NC}"
        echo -n "> "
        read -r MCP_CHOICE
        
        if [ -z "$MCP_CHOICE" ]; then
            echo "   ⏭️  Skipping MCP server installation"
            echo "   ℹ️  You can install servers later with: python3 mcp/install_mcp.py install <server-name>"
        else
            # Install specific servers
            echo -e "${GREEN}📦 Installing selected MCP servers...${NC}"
            python3 mcp/install_mcp.py install $MCP_CHOICE
        fi
    else
        echo -e "${RED}⚠️  Python 3 is required for MCP installation${NC}"
        echo "   Manual installation: python3 mcp/install_mcp.py install <server-name>"
    fi
else
    echo "   ⏭️  Skipping MCP configuration"
    echo "   ℹ️  You can configure servers later with: python3 mcp/install_mcp.py"
fi

# Final summary
echo ""
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo ""
echo "Configuration deployed to: ~/.claude/"
echo "MCP services available at: $(pwd)/mcp/"
echo ""
echo "Next steps:"
echo "1. Review ~/.claude/CLAUDE.md for your global instructions"
echo "2. Configure API keys for MCP servers that require them:"
echo "   - Notion: export NOTION_TOKEN='your-key'"
echo "   - Magic: export TWENTYFIRST_API_KEY='your-key'"
echo "   - MorphLLM: export MORPH_API_KEY='your-key'"
echo "3. Manage MCP servers: python3 mcp/install_mcp.py [list|install|remove|status]"
echo ""
echo -e "${YELLOW}💡 Tip: Restart Claude Code after installing MCP servers${NC}"