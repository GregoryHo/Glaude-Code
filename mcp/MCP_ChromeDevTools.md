# Chrome DevTools MCP Server

**Purpose**: Browser debugging, performance analysis, and automation with AI integration

## Overview
Chrome DevTools MCP is Google's official Model Context Protocol server that enables AI coding agents to control and inspect a live Chrome browser. Launched in September 2025, it provides full access to Chrome DevTools capabilities including performance tracing, DOM inspection, JavaScript execution, and network analysis.

## Key Features
- **Performance Analysis**: Record and analyze performance traces
- **DOM & CSS Inspection**: Inspect and manipulate page structure and styles
- **JavaScript Execution**: Execute arbitrary JavaScript in browser context
- **Console Access**: Read console logs and messages
- **Network Monitoring**: Monitor HTTP requests and responses
- **User Flow Automation**: Automate complex user interactions
- **Screenshots**: Capture page screenshots for visual validation

## Prerequisites
- Node.js 22+ installed
- Current stable Chrome browser
- MCP client (Claude Code, Cursor, Copilot, etc.)

## Installation

### Via Glaude-Code Framework
```bash
# Install Chrome DevTools MCP
python3 mcp/install_mcp.py install chrome-devtools

# Restart Claude Code to activate
```

### Via Claude Code CLI
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

### Manual Configuration
Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

## Configuration Options

### Basic Usage (Default)
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["chrome-devtools-mcp@latest"]
  }
}
```

### Headless Mode
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["chrome-devtools-mcp@latest", "--headless"]
  }
}
```

### Custom Chrome Path
```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["chrome-devtools-mcp@latest"],
    "env": {
      "CHROME_PATH": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    }
  }
}
```

## Available Tools

### Performance Analysis
- `performance_start_trace`: Start recording performance trace
- `performance_stop_trace`: Stop and save performance trace
- `performance_analyze`: Analyze trace for bottlenecks

### DOM & CSS
- `dom_inspect`: Inspect DOM structure
- `dom_query_selector`: Query elements
- `css_get_computed_style`: Get computed CSS properties
- `css_modify`: Modify element styles

### JavaScript
- `js_execute`: Execute JavaScript in page context
- `js_evaluate`: Evaluate expressions and return values

### Console
- `console_get_messages`: Retrieve console logs
- `console_clear`: Clear console

### Network
- `network_get_requests`: Get network request log
- `network_intercept`: Intercept and modify requests

### Screenshots
- `screenshot_capture`: Capture page screenshot
- `screenshot_element`: Capture specific element

## Triggers & Use Cases

### When to Use Chrome DevTools MCP
- Performance debugging and optimization
- Visual regression testing
- DOM manipulation and inspection
- Console error debugging
- Network request analysis
- User flow automation requiring real browser
- JavaScript debugging in live environment

### Choose Chrome DevTools When
- **For debugging**: When you need to inspect running code in browser
- **For performance**: When analyzing page load time, rendering performance
- **For automation**: When Playwright/Selenium is too heavy
- **Not for simple HTTP**: Use WebFetch for simple API calls

## Works Best With
- **Sequential Thinking**: Plan debugging strategy → Chrome DevTools executes inspection
- **Playwright/Selenium**: Chrome DevTools for debugging → Playwright for testing

## Examples

### Performance Analysis
```
"analyze the performance of example.com"
→ Chrome DevTools starts trace, loads page, analyzes bottlenecks

"why is this page loading slowly?"
→ Chrome DevTools records trace, identifies render-blocking resources
```

### DOM Inspection
```
"inspect the header element styling"
→ Chrome DevTools queries header, returns computed styles

"find all buttons on the page"
→ Chrome DevTools queries DOM, returns button elements
```

### Console Debugging
```
"check for JavaScript errors on this page"
→ Chrome DevTools reads console, returns error messages

"what warnings are in the console?"
→ Chrome DevTools filters console messages by level
```

### Network Analysis
```
"show me all API calls made by this page"
→ Chrome DevTools monitors network, returns API requests

"which requests are taking the longest?"
→ Chrome DevTools analyzes network timing
```

## Advantages Over Other Tools

### vs. Playwright MCP
- **Lighter weight**: Faster startup, less resource intensive
- **Better debugging**: Full DevTools Protocol access
- **Performance focus**: Built-in performance analysis tools

### vs. WebFetch
- **Real browser**: Executes JavaScript, renders CSS
- **Interactive**: Can interact with dynamic content
- **Debugging**: Access to console, network, performance data

## Best Practices

1. **Use for Debugging**: Leverage full DevTools capabilities
2. **Performance First**: Start with performance traces for slow pages
3. **Console Monitoring**: Always check console for errors
4. **Network Analysis**: Monitor network for API issues
5. **Selective Screenshots**: Capture evidence of visual bugs

## Common Workflows

### Performance Debugging
1. Start performance trace
2. Load target page
3. Stop trace
4. Analyze for bottlenecks
5. Identify optimization opportunities

### Error Investigation
1. Open page in Chrome DevTools
2. Read console messages
3. Filter by error level
4. Execute JavaScript to inspect state
5. Report findings

### Visual Regression
1. Navigate to page
2. Capture screenshot
3. Compare with baseline
4. Report differences

## Troubleshooting

### Chrome Not Found
```bash
# Set CHROME_PATH environment variable
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

### Connection Issues
```bash
# Ensure Chrome DevTools Protocol port is available (default: 9222)
# Check for conflicting Chrome instances
ps aux | grep chrome
```

### Permission Errors
```bash
# Ensure Chrome has necessary permissions on macOS
# System Preferences → Security & Privacy → Automation
```

## Additional Resources

- [Chrome DevTools Protocol Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Official Blog Post](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Performance Analysis Guide](https://developer.chrome.com/docs/devtools/performance/)
