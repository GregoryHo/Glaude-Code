# Playwright MCP Server

**Purpose**: Cross-browser E2E testing and browser automation with AI integration

## Overview
Playwright MCP is Microsoft's official Model Context Protocol server that enables LLMs and AI agents to interact with web pages through Playwright's powerful browser automation framework. Launched in March 2025, it uses the browser's accessibility tree instead of pixel-based models for deterministic, reliable automation.

## Key Features
- **Cross-Browser Support**: Automate Chromium, Firefox, and WebKit (Safari)
- **Accessibility-Based**: Uses structured data instead of visual cues
- **Auto-Wait**: Automatically waits for elements to be ready
- **Parallel Testing**: Run multiple tests across isolated threads
- **Mobile Testing**: Support for mobile web testing
- **Test Generation**: Record and generate tests from user interactions

## Prerequisites
- Node.js 18+ installed
- MCP client (Claude Code, VS Code, Cursor, etc.)

## Installation

### Via Claude Code CLI
```bash
claude mcp add playwright npx @playwright/mcp@latest
```

### Manual Configuration
Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Configuration Options

### Basic Usage (Default)
```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest"]
  }
}
```

### Headless Mode
```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest", "--headless"]
  }
}
```

### Custom Browser Configuration
```json
{
  "playwright": {
    "command": "npx",
    "args": [
      "@playwright/mcp@latest",
      "--browser=firefox",
      "--viewport-size=1920,1080"
    ]
  }
}
```

## Available Command-Line Options

```bash
--browser <browser>           # Browser to use: chrome, firefox, webkit
--headless                    # Run in headless mode
--viewport-size <size>        # Browser viewport (e.g., "1280,720")
--device <device>            # Emulate device (e.g., "iPhone 15")
--timeout-action <ms>        # Action timeout (default: 5000ms)
--timeout-navigation <ms>    # Navigation timeout (default: 60000ms)
--output-dir <path>          # Directory for output files
```

## Triggers & Use Cases

### When to Use Playwright MCP
- Browser testing and E2E test scenarios
- Visual testing, screenshot, or UI validation requests
- Form submission and user interaction testing
- Cross-browser compatibility validation
- Performance testing requiring real browser rendering
- Accessibility testing with automated WCAG compliance

### Choose Playwright When
- **For real browser interaction**: When you need actual rendering, not just code
- **Over unit tests**: For integration testing, user journeys, visual validation
- **For E2E scenarios**: Login flows, form submissions, multi-page workflows
- **For visual testing**: Screenshot comparisons, responsive design validation
- **Not for code analysis**: Use native Claude for static code review

## Works Best With
- **Sequential Thinking**: Sequential plans test strategy → Playwright executes browser automation
- **Magic UI**: Magic creates UI components → Playwright validates accessibility and behavior

## Examples
```
"test the login flow" → Playwright (browser automation)
"check if form validation works" → Playwright (real user interaction)
"take screenshots of responsive design" → Playwright (visual testing)
"validate accessibility compliance" → Playwright (automated WCAG testing)
"test across Chrome, Firefox, and Safari" → Playwright (cross-browser)
```

## Advantages Over Puppeteer MCP

1. **Multi-Browser**: Test on Chrome, Firefox, and Safari
2. **Better Waiting**: Auto-wait reduces flaky tests
3. **Mobile Support**: Built-in mobile device emulation
4. **Multiple Languages**: APIs for Python, Java, C#, not just JavaScript
5. **Test Runner**: Built-in test framework with parallel execution
6. **Debugging**: Better trace viewer and debugging tools

## Best Practices

1. **Use Auto-Wait**: Let Playwright handle element readiness
2. **Leverage Selectors**: Use data-testid attributes for reliability
3. **Parallel Testing**: Run tests in parallel for speed
4. **Browser Contexts**: Use contexts for test isolation
5. **Network Mocking**: Mock API responses for consistent tests

## Troubleshooting

### Browser Not Launching
```bash
# Install browsers manually
npx playwright install
```

### Timeout Issues
```bash
# Increase timeouts for slower connections
npx @playwright/mcp@latest --timeout-navigation=120000
```

## Additional Resources

- [Official Playwright Documentation](https://playwright.dev)
- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright Test Framework](https://playwright.dev/docs/test-intro)