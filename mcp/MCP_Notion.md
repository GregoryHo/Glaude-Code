# Notion MCP Server

**Purpose**: Rate-limited Notion integration for task management and knowledge base operations

## Triggers
- Task creation and project management requests
- Knowledge base queries and documentation updates
- Note-taking and information organization needs
- Database operations: create, update, query pages
- Workspace synchronization requirements
- Rate limit: 100 operations per hour with automatic queuing

## Choose When
- **For productivity workflows**: Task tracking, project management, documentation
- **Over manual updates**: When you need programmatic Notion access
- **For knowledge management**: Creating and organizing documentation
- **With rate awareness**: Operations are automatically queued if limits are exceeded
- **Not for real-time sync**: Rate limiting makes it unsuitable for instant updates

## Works Best With
- **Sequential**: Sequential plans documentation structure → Notion organizes content
- **Context7**: Context7 provides technical docs → Notion stores for team reference

## Examples
```
"create a task in Notion" → Notion (task management)
"update project documentation" → Notion (knowledge base update)
"query my todo database" → Notion (database operations)
"sync meeting notes" → Notion (information organization)
"analyze code performance" → Sequential (not a Notion task)
"create a UI component" → Magic (not a Notion task)
```

## Configuration
Requires environment variable:
```bash
export NOTION_TOKEN='your-notion-integration-token'
```

## Rate Limiting
- Maximum 100 operations per hour
- Automatic queuing when limit is reached
- Operations logged to `mcp/notion/logs/`
- Retry logic with exponential backoff