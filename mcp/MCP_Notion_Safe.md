# Notion Safe MCP Server

**Purpose**: Enterprise-grade Notion integration with built-in safety features and audit capabilities

## Overview
Production-ready Notion wrapper providing controlled access with comprehensive logging, rate limiting, and safety mechanisms for AI-driven automation. Designed for long-running AI agents and production environments where operation control and audit trails are critical.

## Key Safety Features
- **Rate Limiting**: Controlled operation throughput (100 ops/hour, configurable)
- **Audit Logging**: Complete operation history in JSONL format
- **Batch Processing**: Automatic handling of large content operations
- **Safety Checks**: Pre-execution validation for write operations
- **Error Recovery**: Retry logic with exponential backoff
- **Operation Tracking**: Real-time monitoring and statistics

## Architecture
```
Claude Code
    ↓
Notion Safe Wrapper (mcp/notion-safe/)
    ├── Rate Limiting (100 ops/hour)
    ├── Operation Logging (.notion-logs/)
    ├── Batch Processing (20+ blocks)
    └── Safety Checks
    ↓
Official Notion MCP Server
    ↓
Notion API
```

Custom wrapper layer providing safety guarantees while maintaining full Notion API compatibility.

## Prerequisites
- Node.js 18+ installed
- Notion integration token
- `@notionhq/notion-mcp-server` package installed

## Installation

### Via install_mcp.py
```bash
# Install Notion Safe wrapper
python3 mcp/install_mcp.py install notion-safe

# Verify installation
python3 mcp/install_mcp.py status
```

### Manual Installation
1. Install dependencies:
```bash
cd mcp/notion-safe
npm install
```

2. Add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "notion-safe": {
      "command": "node",
      "args": [
        "${HOME}/GitHub/AI/Glaude-Code/mcp/notion-safe/src/notion-mcp-wrapper.js"
      ],
      "env": {
        "NOTION_TOKEN": "${NOTION_TOKEN}"
      }
    }
  }
}
```

## Triggers
- Long-running automation tasks
- Production AI agent workflows
- Batch documentation updates
- Compliance-required operations
- Multi-agent Notion access
- Continuous integration/deployment documentation
- Automated project tracking
- High-frequency workspace modifications

## Choose When
- **For production environments**: AI automation running continuously
- **For audit requirements**: Need operation traceability and compliance
- **For safety guarantees**: Protecting critical workspaces from runaway operations
- **For controlled access**: Rate-limited operations to prevent API abuse
- **For multi-agent scenarios**: Multiple AI agents accessing same workspace
- **For compliance**: Regulatory audit trails and operation logs

## Works Best With
- **Archon**: Continuous project management automation with full audit trail
- **Sequential**: Multi-step workflows with safe, logged execution
- **Context7**: Bulk documentation imports with operation tracking

## Examples
```
"automate daily standup notes to Notion" → Notion-Safe (recurring automation)
"AI agent manages project dashboard continuously" → Notion-Safe (long-running)
"sync GitHub issues to Notion hourly" → Notion-Safe (scheduled automation)
"bulk import documentation with audit trail" → Notion-Safe (batch + logging)
"multi-agent task assignment and tracking" → Notion-Safe (concurrency control)
"automated sprint planning and retrospectives" → Notion-Safe (production workflow)
```

## Configuration

### Required Environment Variable
```bash
export NOTION_TOKEN='your-notion-integration-token'
```

### Optional Configuration
```bash
# Adjust rate limit (default: 100 operations per hour)
export MAX_OPERATIONS_PER_HOUR=200

# Custom log directory (default: .notion-logs in current working directory)
export NOTION_LOG_DIR="~/logs/notion"

# Disable file logging, keep stderr only (default: enabled)
export LOG_TO_FILE=false
```

## Safety Features Details

### Rate Limiting
**Purpose**: Prevent runaway AI automation from overwhelming Notion API

**How it works**:
- Tracks operations in sliding 1-hour window
- Automatically rejects operations exceeding configured limit
- Provides clear error messages with remaining quota
- Resets automatically as time window slides

**Configuration**:
```bash
# Set custom limit (default: 100)
export MAX_OPERATIONS_PER_HOUR=150
```

**Behavior**:
- Operations are counted at request time
- Failed operations don't count toward limit
- Error message includes current usage and time to reset

### Operation Logging
**Purpose**: Complete audit trail for compliance and debugging

**Log location**: `.notion-logs/operations-{date}.jsonl`

**Log format**:
```json
{
  "timestamp": "2025-01-21T10:30:45.123Z",
  "requestId": "req_abc123",
  "method": "tools/call",
  "tool": "API-post-page",
  "status": "success"
}
```

**Fields captured**:
- `timestamp`: ISO 8601 timestamp
- `requestId`: Unique request identifier
- `method`: MCP protocol method
- `tool`: Notion API tool name
- `status`: `pending`, `success`, or `failed`
- `batchInfo`: Batch metadata (if applicable)

**Viewing logs**:
```bash
# Real-time monitoring
tail -f ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl

# Search for failures
grep '"status":"failed"' ~/.notion-logs/operations-*.jsonl

# Count today's operations
cat ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl | wc -l
```

### Batch Processing
**Purpose**: Handle large content operations without API timeouts

**Trigger**: Automatically activates for operations with 20+ blocks

**Process**:
1. Detects large content operations
2. Splits into batches of 20 items each
3. Processes each batch sequentially
4. 500ms delay between batches to avoid rate limits
5. Logs each batch completion

**Example output**:
```
📦 Splitting large request into 3 batches
📝 Processing batch 1/3 (20 items)
📝 Processing batch 2/3 (20 items)
📝 Processing batch 3/3 (15 items)
✅ All 3 batches sent successfully
```

### Safety Checks
**Purpose**: Validate operations before execution

**Write operations screened**:
- `API-post-page` (Create page)
- `API-patch-page` (Update page properties)
- `API-patch-block-children` (Append blocks)
- `API-update-a-block` (Update block)
- `API-create-a-database` (Create database)
- `API-update-a-database` (Update database)
- `API-delete-a-block` (Delete block)
- `API-create-a-comment` (Create comment)

**Checks performed**:
1. Rate limit validation
2. Request format validation
3. Content size assessment (batch processing decision)

### Error Recovery
**Purpose**: Graceful handling of failures

**Features**:
- Retry logic for transient failures
- Exponential backoff for rate limit errors
- Clear error messages to user
- Failed operations logged separately
- Graceful degradation when wrapper fails (falls through to direct MCP)

## Monitoring & Analytics

### Real-Time Monitoring
```bash
# Watch live operations
tail -f ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl

# Filter by status
tail -f ~/.notion-logs/operations-*.jsonl | grep '"status":"failed"'
```

### Operation Statistics
```bash
# Count operations by status
jq -s 'group_by(.status) | map({status: .[0].status, count: length})' \
  ~/.notion-logs/operations-*.jsonl

# Operations per day
for file in ~/.notion-logs/operations-*.jsonl; do
  echo "$(basename $file): $(wc -l < $file) operations"
done

# Most used tools
jq -s 'group_by(.tool) | map({tool: .[0].tool, count: length}) | sort_by(.count) | reverse' \
  ~/.notion-logs/operations-*.jsonl
```

### Log Maintenance
```bash
# View log size
du -sh ~/.notion-logs/

# Clean logs older than 30 days
find ~/.notion-logs -name "*.jsonl" -mtime +30 -delete

# Archive old logs
tar -czf notion-logs-archive-$(date +%Y%m).tar.gz ~/.notion-logs/*.jsonl
find ~/.notion-logs -name "*.jsonl" -mtime +7 -delete
```

## Production Deployment

### Environment Setup
```bash
# Add to ~/.zshrc or ~/.bashrc
export NOTION_TOKEN='secret_your_integration_token'
export MAX_OPERATIONS_PER_HOUR=150
export NOTION_LOG_DIR="/var/log/notion-mcp"

# Create log directory with proper permissions
mkdir -p /var/log/notion-mcp
chmod 755 /var/log/notion-mcp
```

### Monitoring Setup
```bash
# Set up log rotation (Linux/macOS)
cat > /etc/logrotate.d/notion-mcp <<EOF
/var/log/notion-mcp/*.jsonl {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
}
EOF
```

### Health Checks
```bash
# Check wrapper is running
ps aux | grep notion-mcp-wrapper

# Verify recent operations
test -f ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl && \
  echo "Logging active" || echo "No operations today"

# Check rate limit usage (last hour)
jq -s --arg hour "$(date -u -v-1H +%Y-%m-%dT%H)" \
  'map(select(.timestamp > $hour)) | length' \
  ~/.notion-logs/operations-$(date +%Y-%m-%d).jsonl
```

## Troubleshooting

### Rate Limit Exceeded
```
Error: Rate limit exceeded: 100/100 operations in the last hour
```

**Solutions**:
1. Wait for sliding window to reset
2. Increase limit: `export MAX_OPERATIONS_PER_HOUR=200`
3. Optimize AI prompts to reduce operations
4. Batch operations when possible

### Wrapper Not Starting
**Symptom**: No logs appearing, operations failing

**Diagnosis**:
```bash
# Check if official MCP server is installed
npm list -g @notionhq/notion-mcp-server

# Test wrapper directly
node ~/GitHub/AI/Glaude-Code/mcp/notion-safe/src/notion-mcp-wrapper.js
```

**Solutions**:
```bash
# Install missing dependency
cd ~/GitHub/AI/Glaude-Code/mcp/notion-safe
npm install

# Reinstall official server
npm install -g @notionhq/notion-mcp-server
```

### Logs Not Appearing
**Symptom**: No JSONL files created

**Diagnosis**:
```bash
# Check log directory
ls -la ~/.notion-logs/

# Verify logging enabled
env | grep LOG_TO_FILE
```

**Solutions**:
```bash
# Create log directory
mkdir -p ~/.notion-logs

# Enable file logging
unset LOG_TO_FILE  # or set to true

# Check permissions
chmod 755 ~/.notion-logs
```

### Batch Processing Issues
**Symptom**: Large operations timing out

**Diagnosis**: Check logs for batch messages

**Solutions**:
- Wrapper automatically batches operations > 20 blocks
- If still timing out, reduce content size
- Check network connectivity
- Verify Notion API status

### Permission Errors
**Symptom**: Operations fail with permission denied

**Solution**: Same as official Notion MCP:
1. Open target page in Notion
2. Click "..." menu → "Add connections"
3. Select your integration
4. Grant access

## Session Statistics
When wrapper exits (Ctrl+C), displays summary:
```
Session Statistics:
  • Total operations: 45
  • Successful: 42
  • Failed: 3

Shutting down...
```

## Security Best Practices

1. **Token Storage**: Never commit tokens to version control
2. **Log Security**: Protect log directory (contains operation history)
3. **Rate Limits**: Set conservative limits for untested AI workflows
4. **Access Control**: Use integration-level permissions in Notion
5. **Log Rotation**: Implement log rotation to prevent disk exhaustion
6. **Monitoring**: Regularly review operation logs for anomalies

## Additional Resources
- [Wrapper Source Code](../notion-safe/src/notion-mcp-wrapper.js)
- [Implementation Guide](../notion-safe/IMPLEMENTATION.md)
- [Security Guide](../notion-safe/docs/security-guide.md)
- [Lessons Learned](../notion-safe/LESSONS_LEARNED.md)
- [Notion API Documentation](https://developers.notion.com)
