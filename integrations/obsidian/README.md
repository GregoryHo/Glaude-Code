# Obsidian Integration

File-based knowledge management integration using Claude Code's native tools.

## Overview

This integration allows Claude Code to interact with Obsidian vaults without requiring an MCP server. It uses:
- **Direct file access** for reading, writing, and searching notes
- **Obsidian URI scheme** for opening notes in the Obsidian app

## Why No MCP?

While several community MCP servers exist for Obsidian, direct file access provides:
- ✅ **Zero dependencies**: No external services required
- ✅ **Better security**: No third-party code handling your notes
- ✅ **Faster performance**: Direct filesystem access
- ✅ **Full compatibility**: Works with all Obsidian features

## Prerequisites

- Obsidian installed (for URI scheme functionality)
- Access to your Obsidian vault directory
- Claude Code with native file tools (Read, Write, Grep, Glob)

## Setup

### 1. Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Obsidian vault configuration
export OBSIDIAN_VAULT_PATH="$HOME/Documents/MyVault"
export OBSIDIAN_VAULT_NAME="MyVault"
```

Replace with your actual vault path and name.

### 2. Reload Shell Configuration

```bash
source ~/.zshrc  # or ~/.bashrc
```

### 3. Verify Setup

```bash
echo $OBSIDIAN_VAULT_PATH
# Should output: /Users/yourname/Documents/MyVault

ls "$OBSIDIAN_VAULT_PATH"
# Should list your vault contents
```

## Usage

### Read Notes

```bash
# Read a specific note
Read ${OBSIDIAN_VAULT_PATH}/DailyNotes/2025-01-19.md

# Read with Claude Code
Read /Users/yourname/Documents/MyVault/Projects/AI-Research.md
```

### Search Vault

```bash
# Search for keyword
Grep "TODO" --path ${OBSIDIAN_VAULT_PATH}

# Search with context (3 lines before and after)
Grep "meeting notes" --path ${OBSIDIAN_VAULT_PATH} -C 3

# Search for tags
Grep "tag:#important" --path ${OBSIDIAN_VAULT_PATH}

# Case-insensitive search
Grep "project" --path ${OBSIDIAN_VAULT_PATH} -i
```

### Find Files

```bash
# Find all markdown files
Glob "${OBSIDIAN_VAULT_PATH}/**/*.md"

# Find notes in specific folder
Glob "${OBSIDIAN_VAULT_PATH}/Projects/*.md"

# Find daily notes
Glob "${OBSIDIAN_VAULT_PATH}/DailyNotes/2025-*.md"
```

### Create/Update Notes

```bash
# Create a new note
Write ${OBSIDIAN_VAULT_PATH}/NewNote.md "# New Note\n\nContent here"

# Update existing note (requires Read first)
Read ${OBSIDIAN_VAULT_PATH}/ExistingNote.md
# Then use Edit tool to modify
```

### Open in Obsidian

```bash
# Open specific note
Bash open "obsidian://open?vault=${OBSIDIAN_VAULT_NAME}&file=note.md"

# Search in Obsidian
Bash open "obsidian://search?vault=${OBSIDIAN_VAULT_NAME}&query=tag:#project"

# Create new note
Bash open "obsidian://new?vault=${OBSIDIAN_VAULT_NAME}&name=NewNote"
```

## Common Workflows

See [WORKFLOWS.md](./WORKFLOWS.md) for detailed examples and common use cases.

## Obsidian URI Scheme Reference

### Open Note
```
obsidian://open?vault=<vault>&file=<file>
```

### Search
```
obsidian://search?vault=<vault>&query=<query>
```

### Create Note
```
obsidian://new?vault=<vault>&name=<name>&content=<content>
```

### Advanced Actions
```
obsidian://advanced-uri?vault=<vault>&daily=true
obsidian://advanced-uri?vault=<vault>&commandid=<command>
```

Full documentation: https://help.obsidian.md/Extending+Obsidian/Obsidian+URI

## Working with Frontmatter

Obsidian notes can have YAML frontmatter. Claude Code can read and modify it:

```markdown
---
title: My Note
tags: [project, important]
created: 2025-01-19
---

# Content here
```

Use Read and Edit tools to work with frontmatter-enabled notes.

## Tips & Best Practices

### 1. Use Absolute Paths
Always use `${OBSIDIAN_VAULT_PATH}` or absolute paths to avoid ambiguity.

### 2. Preserve Frontmatter
When editing notes, preserve existing YAML frontmatter to avoid breaking Obsidian metadata.

### 3. Batch Operations
Use Grep to find multiple files, then process them in batch.

### 4. Link Preservation
When modifying notes, preserve Obsidian's `[[wikilinks]]` format.

### 5. Tag Format
Obsidian tags use `#tag` format. Search with `Grep "tag:#tagname"`.

## External Integration

Other projects can use this integration by:

1. **Copying this directory**:
   ```bash
   cp -r integrations/obsidian /path/to/your/project/
   ```

2. **Setting environment variables**:
   ```bash
   export OBSIDIAN_VAULT_PATH="/your/vault/path"
   export OBSIDIAN_VAULT_NAME="YourVault"
   ```

3. **Following the examples** in WORKFLOWS.md

## Troubleshooting

### Vault Not Found
```bash
# Verify path is correct
ls "${OBSIDIAN_VAULT_PATH}"

# Check environment variable
echo $OBSIDIAN_VAULT_PATH
```

### URI Scheme Not Working
- Ensure Obsidian is installed
- Verify vault name matches exactly (case-sensitive)
- On macOS: System Preferences → Security & Privacy → Automation

### Permission Errors
```bash
# Check vault directory permissions
ls -la "${OBSIDIAN_VAULT_PATH}"

# Ensure read/write access
chmod u+rw "${OBSIDIAN_VAULT_PATH}"/*.md
```

## Limitations

- **No plugin access**: Can't invoke Obsidian plugins directly
- **No live sync**: Changes require manual refresh in Obsidian
- **No database queries**: Can't query Obsidian's internal database

For these advanced features, consider using an Obsidian MCP server with the Local REST API plugin.

## See Also

- [WORKFLOWS.md](./WORKFLOWS.md) - Common operation examples
- [Obsidian URI Documentation](https://help.obsidian.md/Extending+Obsidian/Obsidian+URI)
- [Obsidian Help](https://help.obsidian.md/)
