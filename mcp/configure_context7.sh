#!/bin/bash

# Context7 API Key Configuration Script

echo "🔧 Context7 API Key Configuration"
echo "=================================="
echo ""
echo "Context7 works without an API key but provides higher rate limits with one."
echo "Get your API key at: https://context7.com/dashboard"
echo ""

# Check if API key is already set
if [ ! -z "$CONTEXT7_API_KEY" ]; then
    echo "✓ API key is already set in environment"
    echo ""
    read -p "Do you want to update it? (y/n): " UPDATE_KEY
    if [[ ! "$UPDATE_KEY" =~ ^[Yy]$ ]]; then
        echo "Keeping existing API key"
        exit 0
    fi
fi

# Get API key from user
echo "Please enter your Context7 API key:"
read -s API_KEY
echo ""

if [ -z "$API_KEY" ]; then
    echo "❌ No API key provided"
    exit 1
fi

# Determine shell config file
if [ -n "$ZSH_VERSION" ] || [ -f ~/.zshrc ]; then
    SHELL_CONFIG=~/.zshrc
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ] || [ -f ~/.bashrc ]; then
    SHELL_CONFIG=~/.bashrc
    SHELL_NAME="bash"
else
    SHELL_CONFIG=~/.profile
    SHELL_NAME="profile"
fi

# Check if the export already exists
if grep -q "export CONTEXT7_API_KEY=" "$SHELL_CONFIG" 2>/dev/null; then
    echo "📝 Updating existing Context7 API key in $SHELL_CONFIG"
    # Use sed to update the existing line
    sed -i.bak "s/export CONTEXT7_API_KEY=.*/export CONTEXT7_API_KEY='$API_KEY'/" "$SHELL_CONFIG"
else
    echo "📝 Adding Context7 API key to $SHELL_CONFIG"
    echo "" >> "$SHELL_CONFIG"
    echo "# Context7 MCP Server API Key" >> "$SHELL_CONFIG"
    echo "export CONTEXT7_API_KEY='$API_KEY'" >> "$SHELL_CONFIG"
fi

# Export for current session
export CONTEXT7_API_KEY="$API_KEY"

echo "✅ API key configured successfully!"
echo ""

# Update context7 in Claude Code
echo "🔄 Updating context7 configuration..."
python3 "$(dirname "$0")/install_mcp.py" install context7 --force

echo ""
echo "✅ Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source $SHELL_CONFIG"
echo "2. Restart Claude Code to use the updated configuration"
echo ""
echo "Test with: echo \$CONTEXT7_API_KEY"