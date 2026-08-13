# Notion MCP Server

**Purpose**: Official Notion integration for task management and knowledge base operations

## Overview
Official MCP server providing direct access to Notion API for workspace automation, enabling seamless integration between AI agents and Notion workspaces.

## Key Features
- Full Notion API access
- Database operations (create, query, update)
- Page and block management
- Real-time workspace interaction
- Complete feature coverage
- Native Notion API performance

## Prerequisites
- Node.js 18+ installed
- Notion integration token
- Notion workspace with integration enabled

## Installation

### Via install_mcp.py
```bash
# Install Notion MCP server
python3 mcp/install_mcp.py install notion

# Verify installation
python3 mcp/install_mcp.py status
```

### Manual Configuration
Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "${NOTION_TOKEN}"
      }
    }
  }
}
```

## Triggers
- Task creation and project management requests
- Knowledge base and documentation updates
- Database operations: create, update, query
- Page and block manipulation
- Workspace organization and content structuring
- Note-taking and information management

## Choose When
- **For Notion integration**: Direct workspace access and automation
- **For task management**: Creating and tracking tasks, projects, databases
- **For knowledge base**: Documentation organization and team collaboration
- **For automation**: Programmatic Notion operations and workflows
- **For productivity**: Centralized information management

## Works Best With
- **Archon**: Archon manages projects → Notion stores documentation
- **Sequential**: Sequential plans structure → Notion organizes content
- **Context7**: Context7 fetches docs → Notion stores for reference

## Examples
```
"create a task in Notion" → Notion (task creation)
"update project documentation" → Notion (knowledge base update)
"query my todo database" → Notion (database query)
"organize meeting notes" → Notion (content organization)
"create a new project page" → Notion (page creation)
"add blocks to existing page" → Notion (content append)
"search workspace for keyword" → Notion (search operation)
```

## Configuration

### Required Environment Variable
```bash
export NOTION_TOKEN='your-notion-integration-token'
```

### Getting Your Notion Token
1. Visit [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Configure integration settings
4. Copy the "Internal Integration Token"
5. Add integration to your workspace pages

### Workspace Setup
After creating integration:
1. Open a Notion page
2. Click "..." menu → "Add connections"
3. Select your integration
4. Grant access to specific pages/databases

## Available Operations

### Database Operations
- Create databases
- Query database contents
- Update database properties
- Filter and sort queries

### Page Operations
- Create new pages
- Update page properties
- Append blocks to pages
- Archive pages

### Block Operations
- Create various block types (text, headings, lists, etc.)
- Update existing blocks
- Delete blocks
- Retrieve block children

### Search & Query
- Search workspace content
- Filter by type, property, date
- Full-text search capabilities

### Comments
- Create comments on pages
- Retrieve comment threads
- Discussion management

## Common Use Cases

### Project Management
```
"create a project tracker database with status, assignee, and deadline"
"add a new task to Sprint 1 with high priority"
"query all tasks assigned to me that are overdue"
```

### Documentation
```
"create a technical spec page for the new API endpoint"
"update the installation guide with new prerequisites"
"organize all backend docs under Architecture section"
```

### Team Collaboration
```
"create meeting notes template with action items"
"share research findings in the team wiki"
"sync GitHub issues to Notion project board"
```

## Best Practices

1. **Integration Scope**: Only grant access to necessary pages/databases
2. **Token Security**: Store token in environment variables, never commit to code
3. **Workspace Organization**: Use consistent naming and structure
4. **API Limits**: Be aware of Notion's API rate limits (3 requests/sec)
5. **Page Connections**: Remember to connect integration to pages before operations

## Troubleshooting

### Token Authentication Failed
```
Error: Unauthorized - check your NOTION_TOKEN
```
**Solution**: Verify token is correct and hasn't been regenerated

### Page Not Found
```
Error: Could not find page
```
**Solution**: Ensure integration is connected to the target page

### Rate Limit Errors
```
Error: Rate limit exceeded
```
**Solution**: Notion API has rate limits. Wait and retry, or implement backoff logic

### Permission Denied
```
Error: Insufficient permissions
```
**Solution**: Add integration to page via "Add connections" in page settings

## Additional Resources
- [Official Notion API Docs](https://developers.notion.com)
- [Create Integration](https://www.notion.so/my-integrations)
- [API Reference](https://developers.notion.com/reference/intro)
- [Community Examples](https://developers.notion.com/docs/examples)
- [Rate Limits Guide](https://developers.notion.com/reference/request-limits)
