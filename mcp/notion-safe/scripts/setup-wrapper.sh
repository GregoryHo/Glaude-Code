#!/bin/bash

# Notion MCP Wrapper 設定腳本
# 使用官方 MCP Server + 安全包裝層

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "╔══════════════════════════════════════════╗"
echo "║   Notion MCP Wrapper Setup               ║"
echo "║   (Official MCP + Safety Layer)          ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 步驟 1: 檢查系統需求
echo -e "${YELLOW}[1/5]${NC} Checking requirements..."

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js first: https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓${NC} Node.js $(node -v)"

if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude Code CLI is not installed${NC}"
    echo "Please install Claude Code first"
    exit 1
fi
echo -e "${GREEN}✓${NC} Claude Code CLI"

# 步驟 2: 安裝官方 Notion MCP Server
echo -e "\n${YELLOW}[2/5]${NC} Installing official Notion MCP Server..."

# 優先使用本地安裝
if [ -f "$PROJECT_DIR/node_modules/.bin/notion-mcp-server" ]; then
    echo -e "${GREEN}✓${NC} Notion MCP Server already installed locally"
elif npm list -g @notionhq/notion-mcp-server &>/dev/null; then
    echo -e "${GREEN}✓${NC} Notion MCP Server already installed globally"
else
    echo "Installing @notionhq/notion-mcp-server locally..."
    cd "$PROJECT_DIR" && npm install
    echo -e "${GREEN}✓${NC} Notion MCP Server installed"
fi

# 確認安裝路徑（優先本地）
if [ -f "$PROJECT_DIR/node_modules/.bin/notion-mcp-server" ]; then
    MCP_PATH="$PROJECT_DIR/node_modules/.bin/notion-mcp-server"
    echo -e "${GREEN}✓${NC} Using local MCP Server: $MCP_PATH"
else
    MCP_PATH=$(which notion-mcp-server 2>/dev/null || echo "")
    if [ -z "$MCP_PATH" ]; then
        echo -e "${RED}❌ Cannot find notion-mcp-server${NC}"
        echo "Please run: cd $PROJECT_DIR && npm install"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Using global MCP Server: $MCP_PATH"
fi

# 步驟 3: 設定 Wrapper
echo -e "\n${YELLOW}[3/5]${NC} Setting up wrapper..."

# 設定執行權限
chmod +x "$PROJECT_DIR/src/notion-mcp-wrapper.js"
echo -e "${GREEN}✓${NC} Wrapper configured"

# 步驟 4: 檢查環境變數
echo -e "\n${YELLOW}[4/5]${NC} Checking environment..."

if [ -z "$NOTION_TOKEN" ]; then
    echo -e "${YELLOW}⚠${NC}  NOTION_TOKEN not set in environment"
    echo "   Add to ~/.bash_profile or ~/.zshrc:"
    echo "   export NOTION_TOKEN=\"your_api_key_here\""
else
    echo -e "${GREEN}✓${NC} NOTION_TOKEN is configured"
fi

# 步驟 5: 建立日誌目錄
echo -e "\n${YELLOW}[5/5]${NC} Creating log directory..."

if [ ! -d "$PROJECT_DIR/logs" ]; then
    mkdir -p "$PROJECT_DIR/logs"
    echo -e "${GREEN}✓${NC} Log directory created"
else
    echo -e "${GREEN}✓${NC} Log directory exists"
fi

# 完成訊息
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Setup Complete!                        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Get your Notion API Key:"
echo "   • Go to https://www.notion.so/my-integrations"
echo "   • Create a new integration"
echo "   • Copy the API key"
echo ""
echo "2. Set environment variable:"
echo "   export NOTION_TOKEN=\"your_api_key_here\""
echo "   • Add to ~/.bash_profile or ~/.zshrc for persistence"
echo ""
echo "3. Configure Claude Code:"
echo ""
echo -e "${YELLOW}# Add the wrapper service:${NC}"
echo "claude mcp add notion-safe \"$PROJECT_DIR/src/notion-mcp-wrapper.js\""
echo ""
echo "4. Verify connection:"
echo "   claude mcp list"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Safety Features:${NC}"
echo "  ✓ Rate limiting (100 ops/hour by default)"
echo "  ✓ Operation logging"
echo "  ✓ Optional zone isolation"
echo "  ✓ Uses official MCP server"
echo ""
echo -e "${YELLOW}Note:${NC} The wrapper adds safety without removing functionality"
echo "