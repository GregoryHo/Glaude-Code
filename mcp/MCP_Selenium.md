# Selenium MCP Server

**Purpose**: Cross-browser web automation and testing with Selenium WebDriver

## Overview
Selenium MCP Server bridges the Model Context Protocol with Selenium WebDriver, enabling AI agents to perform browser automation using the industry-standard Selenium framework. This integration allows LLMs to leverage Selenium's mature ecosystem for comprehensive web testing and automation tasks.

## Key Features
- **WebDriver Protocol**: Industry-standard browser automation protocol
- **Cross-Browser Support**: Chrome, Firefox, Safari, Edge, and more
- **Grid Support**: Distributed testing across multiple machines
- **Legacy Support**: Works with older web applications
- **Extensive Language Bindings**: Java, Python, JavaScript, C#, Ruby
- **Mobile Testing**: Via Appium integration

## Prerequisites
- Node.js 18+ installed
- Browser drivers (ChromeDriver, GeckoDriver, etc.)
- MCP client (Claude Code, VS Code, Cursor, etc.)

## Installation

### Via NPM
```bash
npm install -g @modelcontextprotocol/server-selenium
```

### Manual Configuration
Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "selenium": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-selenium"]
    }
  }
}
```

## Configuration Options

### Basic Usage (Chrome)
```json
{
  "selenium": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-selenium"]
  }
}
```

### Firefox Configuration
```json
{
  "selenium": {
    "command": "npx",
    "args": [
      "@modelcontextprotocol/server-selenium",
      "--browser=firefox"
    ]
  }
}
```

### Headless Mode
```json
{
  "selenium": {
    "command": "npx",
    "args": [
      "@modelcontextprotocol/server-selenium",
      "--headless"
    ]
  }
}
```

### Custom WebDriver Options
```json
{
  "selenium": {
    "command": "npx",
    "args": [
      "@modelcontextprotocol/server-selenium",
      "--browser=chrome",
      "--window-size=1920,1080",
      "--disable-gpu"
    ]
  }
}
```

## Selenium vs Playwright Comparison

### Choose Selenium When:
- **Legacy Systems**: Working with older web applications
- **Enterprise Environments**: Where Selenium is already established
- **Grid Testing**: Need distributed testing infrastructure
- **WebDriver Compliance**: Require W3C WebDriver protocol
- **Team Expertise**: Team is already familiar with Selenium

### Choose Playwright When:
- **Modern Applications**: Building new test suites
- **Speed Priority**: Need faster test execution
- **Auto-Wait Features**: Want automatic element waiting
- **Better Debugging**: Need trace viewer and debugging tools
- **Cross-Browser Testing**: Consistent API across browsers

## Common Use Cases

### 1. Basic Navigation and Interaction
```javascript
// Navigate to a page
driver.get('https://example.com');

// Find and interact with elements
const element = driver.findElement(By.id('username'));
element.sendKeys('testuser');

// Click buttons
driver.findElement(By.css('button[type="submit"]')).click();
```

### 2. Wait Strategies
```javascript
// Explicit wait
const wait = new WebDriverWait(driver, 10);
wait.until(elementLocated(By.id('result')));

// Implicit wait
driver.manage().setTimeouts({ implicit: 5000 });
```

### 3. Form Automation
```javascript
// Fill forms
driver.findElement(By.name('email')).sendKeys('test@example.com');
driver.findElement(By.name('password')).sendKeys('password123');
driver.findElement(By.xpath('//button[@type="submit"]')).click();
```

### 4. Screenshot Capture
```javascript
// Take screenshot
const screenshot = await driver.takeScreenshot();
fs.writeFileSync('screenshot.png', screenshot, 'base64');
```

### 5. JavaScript Execution
```javascript
// Execute JavaScript in browser
const result = await driver.executeScript('return document.title');
```

## Locator Strategies

Selenium supports multiple element location strategies:
- **ID**: `By.id('element-id')`
- **Name**: `By.name('element-name')`
- **Class Name**: `By.className('class-name')`
- **CSS Selector**: `By.css('.class #id')`
- **XPath**: `By.xpath('//div[@class="example"]')`
- **Link Text**: `By.linkText('Click here')`
- **Partial Link Text**: `By.partialLinkText('Click')`
- **Tag Name**: `By.tagName('button')`

## Best Practices

1. **Use Explicit Waits**: Avoid Thread.sleep(), use WebDriverWait
2. **Page Object Model**: Organize tests with POM pattern
3. **Unique Locators**: Use IDs and data attributes when possible
4. **Error Handling**: Implement proper try-catch blocks
5. **Driver Management**: Properly quit drivers after tests

## Troubleshooting

### Driver Not Found
```bash
# Install ChromeDriver
npm install -g chromedriver

# Or download manually from
# https://chromedriver.chromium.org/
```

### Browser Version Mismatch
```bash
# Check Chrome version
google-chrome --version

# Download matching ChromeDriver version
```

### Timeout Issues
```javascript
// Increase timeout
driver.manage().setTimeouts({
  implicit: 10000,
  pageLoad: 30000,
  script: 30000
});
```

## Selenium Grid Setup

For distributed testing:
```bash
# Start hub
java -jar selenium-server.jar hub

# Start node
java -jar selenium-server.jar node --hub http://localhost:4444
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run Selenium Tests
  run: |
    npm install @modelcontextprotocol/server-selenium
    npm test
```

### Jenkins Example
```groovy
stage('Selenium Tests') {
  steps {
    sh 'npm run selenium-tests'
  }
}
```

## Additional Resources

- [Official Selenium Documentation](https://www.selenium.dev/documentation/)
- [WebDriver W3C Specification](https://www.w3.org/TR/webdriver/)
- [Selenium Grid Documentation](https://www.selenium.dev/documentation/grid/)
- [ChromeDriver Documentation](https://chromedriver.chromium.org/)

## Version Compatibility

- Selenium 4.x: Full W3C WebDriver support
- Chrome: Requires matching ChromeDriver version
- Firefox: Requires GeckoDriver 0.30+
- Safari: Built-in SafariDriver (macOS only)
- Edge: Requires Edge WebDriver