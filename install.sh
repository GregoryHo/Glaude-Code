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

mkdir -p ~/.claude

# Backups are scoped to the files this script actually writes.
# A full `cp -r ~/.claude` would copy gigabytes of sessions, jobs and plugins.
BACKUP_DIR=~/.claude.backup.$(date +%Y%m%d_%H%M%S)

backup_file() {
    local target="$1"
    local rel="${target#$HOME/.claude/}"
    mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
    cp "$target" "$BACKUP_DIR/$rel"
    echo "   📦 backed up to $BACKUP_DIR/$rel"
}

# Never overwrite silently: show what would change and let the user decide.
deploy_file() {
    local src="$1"
    local dest="$2"
    local name="${dest#$HOME/.claude/}"

    [ -f "$src" ] || return 0

    if [ ! -e "$dest" ]; then
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
        echo "   ✓ $name deployed (new)"
        return 0
    fi

    if cmp -s "$src" "$dest"; then
        echo "   = $name unchanged"
        return 0
    fi

    echo ""
    echo -e "${YELLOW}⚠️  $name already exists and differs from this repository:${NC}"
    diff -u "$dest" "$src" | head -40 || true
    echo ""
    echo -e "${YELLOW}Overwrite $name? Your version is backed up first. (y/n)${NC}"
    read -r OVERWRITE_REPLY
    if [[ "$OVERWRITE_REPLY" =~ ^[Yy]$ ]]; then
        backup_file "$dest"
        cp "$src" "$dest"
        echo "   ✓ $name deployed"
    else
        echo "   ⏭️  kept your existing $name"
    fi
}

# Deploy every file under a directory, preserving relative layout
deploy_dir() {
    local srcdir="$1"
    local destdir="$2"
    [ -d "$srcdir" ] || return 0

    # Collect first so the confirmation prompt keeps its own stdin
    local files=()
    local f
    while IFS= read -r f; do
        files+=("$f")
    done < <(find "$srcdir" -type f)

    [ ${#files[@]} -eq 0 ] && return 0

    local src
    for src in "${files[@]}"; do
        deploy_file "$src" "$destdir/${src#$srcdir/}"
    done
}

# Deploy core configuration files
echo -e "${GREEN}📄 Deploying core configuration files...${NC}"

deploy_file "core/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
deploy_file "core/settings.json" "$HOME/.claude/settings.json"
deploy_file "core/personal-context.md" "$HOME/.claude/personal-context.md"

# Deploy always-loaded rules and output styles
if [ -d "core/rules" ] || [ -d "core/output-styles" ]; then
    echo -e "${GREEN}📚 Deploying rules and output styles...${NC}"
    deploy_dir "core/rules" "$HOME/.claude/rules"
    deploy_dir "core/output-styles" "$HOME/.claude/output-styles"
fi

# Deploy agents if directory exists
if [ -d "agents" ] && [ "$(ls -A agents)" ]; then
    echo -e "${GREEN}🤖 Deploying custom agents...${NC}"
    deploy_dir "agents" "$HOME/.claude/agents"
fi

if [ -d "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}📦 Replaced files were backed up to $BACKUP_DIR${NC}"
fi

# Create MCP configuration
echo -e "${GREEN}⚙️  Configuring MCP services...${NC}"

# Generate the reference file, then deploy it through the same confirmation path
MCP_CONFIG_TMP=$(mktemp)
trap 'rm -f "$MCP_CONFIG_TMP"' EXIT
cat > "$MCP_CONFIG_TMP" << EOF
{
  "comment": "MCP services configuration",
  "services": {
    "notion-safe": {
      "description": "Notion API with rate limiting",
      "path": "$(pwd)/mcp/notion-safe/src/notion-mcp-wrapper.js"
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
deploy_file "$MCP_CONFIG_TMP" "$HOME/.claude/mcp-config.json"

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