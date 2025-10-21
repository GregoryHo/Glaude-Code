# Obsidian Workflows

Common operations and examples for working with Obsidian vaults using Claude Code.

## Table of Contents

- [Daily Notes](#daily-notes)
- [Project Management](#project-management)
- [Knowledge Base Search](#knowledge-base-search)
- [Batch Operations](#batch-operations)
- [Tag Management](#tag-management)
- [Link Analysis](#link-analysis)

---

## Daily Notes

### Create Today's Daily Note

```bash
# Generate today's date
TODAY=$(date +%Y-%m-%d)

# Create daily note with template
Write ${OBSIDIAN_VAULT_PATH}/DailyNotes/${TODAY}.md "---
date: ${TODAY}
tags: [daily]
---

# ${TODAY}

## Tasks
- [ ]

## Notes

## Meetings
"

# Open in Obsidian
open "obsidian://open?vault=${OBSIDIAN_VAULT_NAME}&file=DailyNotes/${TODAY}.md"
```

### Review This Week's Notes

```bash
# Find this week's daily notes
WEEK_START=$(date -v-Mon +%Y-%m-%d)
Glob "${OBSIDIAN_VAULT_PATH}/DailyNotes/${WEEK_START:0:7}-*.md"

# Search for incomplete tasks this week
Grep "- \[ \]" --path ${OBSIDIAN_VAULT_PATH}/DailyNotes/ -n
```

---

## Project Management

### Find All Project Notes

```bash
# List all project files
Glob "${OBSIDIAN_VAULT_PATH}/Projects/**/*.md"

# Search for active projects
Grep "status: active" --path ${OBSIDIAN_VAULT_PATH}/Projects/
```

### Create New Project Note

```bash
# Project template
PROJECT_NAME="AI-Agent-System"

Write ${OBSIDIAN_VAULT_PATH}/Projects/${PROJECT_NAME}.md "---
title: ${PROJECT_NAME}
status: active
created: $(date +%Y-%m-%d)
tags: [project]
---

# ${PROJECT_NAME}

## Overview

## Goals

## Tasks
- [ ]

## Resources

## Notes
"
```

### Track Project TODOs

```bash
# Find all TODOs in project notes
Grep "- \[ \]" --path ${OBSIDIAN_VAULT_PATH}/Projects/ -n

# Find completed tasks
Grep "- \[x\]" --path ${OBSIDIAN_VAULT_PATH}/Projects/ -n

# Search for high-priority items
Grep "priority: high" --path ${OBSIDIAN_VAULT_PATH}/Projects/
```

---

## Knowledge Base Search

### Search by Topic

```bash
# Search for machine learning notes
Grep "machine learning" --path ${OBSIDIAN_VAULT_PATH} -i

# Search with context (3 lines before and after)
Grep "transformer architecture" --path ${OBSIDIAN_VAULT_PATH} -C 3

# Search in specific folder
Grep "API design" --path ${OBSIDIAN_VAULT_PATH}/TechnicalNotes/
```

### Find Notes by Tag

```bash
# Find all notes tagged with #research
Grep "#research" --path ${OBSIDIAN_VAULT_PATH}

# Find notes with multiple tags
Grep "#AI.*#research" --path ${OBSIDIAN_VAULT_PATH}

# List all unique tags (requires processing)
Grep "#[a-zA-Z0-9_-]+" --path ${OBSIDIAN_VAULT_PATH} -o
```

### Find Recent Notes

```bash
# Find notes modified in the last 7 days
find ${OBSIDIAN_VAULT_PATH} -name "*.md" -mtime -7

# Sort by modification time
ls -lt ${OBSIDIAN_VAULT_PATH}/**/*.md | head -10
```

---

## Batch Operations

### Add Tag to Multiple Notes

```bash
# Find notes about AI
Grep "artificial intelligence" --path ${OBSIDIAN_VAULT_PATH} --files-with-matches

# For each file, add #AI tag if not present
# (Use Read and Edit tools for each file)
```

### Update Frontmatter Across Notes

```bash
# Find all project notes
PROJECT_FILES=$(Glob "${OBSIDIAN_VAULT_PATH}/Projects/*.md")

# For each file, read and update status field
# (Use Read and Edit tools)
```

### Generate Index File

```bash
# Create an index of all project notes
Write ${OBSIDIAN_VAULT_PATH}/Projects/INDEX.md "# Project Index

Generated: $(date)

## Active Projects

"

# Append list of projects
Glob "${OBSIDIAN_VAULT_PATH}/Projects/*.md"
# Process results and append to INDEX.md
```

---

## Tag Management

### List All Tags

```bash
# Extract all tags from vault
Grep -o "#[a-zA-Z0-9_/-]+" --path ${OBSIDIAN_VAULT_PATH} | sort | uniq

# Count tag usage
Grep -o "#[a-zA-Z0-9_/-]+" --path ${OBSIDIAN_VAULT_PATH} | sort | uniq -c | sort -nr
```

### Find Untagged Notes

```bash
# Find notes without tags in frontmatter
Grep -L "tags:" --path ${OBSIDIAN_VAULT_PATH}

# Find notes without inline tags
Grep -L "#[a-zA-Z0-9_-]" --path ${OBSIDIAN_VAULT_PATH}
```

### Rename Tags

```bash
# Find all notes with old tag
Grep "#old-tag" --path ${OBSIDIAN_VAULT_PATH} --files-with-matches

# For each file:
# 1. Read the file
# 2. Edit to replace #old-tag with #new-tag
# 3. Verify the change
```

---

## Link Analysis

### Find Broken Links

```bash
# Find all wikilinks
Grep "\[\[.*\]\]" --path ${OBSIDIAN_VAULT_PATH} -o

# Check if linked files exist
# (Requires processing the wikilink format)
```

### Find Backlinks

```bash
# Find all notes linking to a specific note
TARGET_NOTE="AI-Research"
Grep "\[\[${TARGET_NOTE}\]\]" --path ${OBSIDIAN_VAULT_PATH}

# Find all notes linking to current note (with aliases)
Grep "\[\[${TARGET_NOTE}.*\]\]" --path ${OBSIDIAN_VAULT_PATH}
```

### Create Link Graph

```bash
# Extract all links from a note
Read ${OBSIDIAN_VAULT_PATH}/Projects/AI-Agent.md
# Parse [[wikilinks]] to build connection map
```

---

## Advanced Workflows

### Meeting Notes Workflow

```bash
# Create meeting note with template
MEETING_DATE=$(date +%Y-%m-%d)
MEETING_TIME=$(date +%H:%M)

Write ${OBSIDIAN_VAULT_PATH}/Meetings/${MEETING_DATE}-meeting.md "---
date: ${MEETING_DATE}
time: ${MEETING_TIME}
tags: [meeting]
attendees: []
---

# Meeting - ${MEETING_DATE}

## Agenda

## Discussion

## Action Items
- [ ]

## Next Steps
"

# Open in Obsidian
open "obsidian://open?vault=${OBSIDIAN_VAULT_NAME}&file=Meetings/${MEETING_DATE}-meeting.md"
```

### Research Note Compilation

```bash
# Find all research notes on a topic
TOPIC="Large Language Models"
Grep -i "${TOPIC}" --path ${OBSIDIAN_VAULT_PATH} -l

# Create compilation note
Write ${OBSIDIAN_VAULT_PATH}/Compilations/${TOPIC}-compilation.md "# ${TOPIC} - Research Compilation

Generated: $(date)

## Sources

"

# Append found notes
# (Process grep results and add links)
```

### Weekly Review

```bash
# Generate weekly review note
WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)

Write ${OBSIDIAN_VAULT_PATH}/Reviews/${YEAR}-W${WEEK_NUM}.md "---
date: $(date +%Y-%m-%d)
week: ${WEEK_NUM}
tags: [review, weekly]
---

# Week ${WEEK_NUM} - ${YEAR}

## Completed Tasks
$(Grep "- \[x\]" --path ${OBSIDIAN_VAULT_PATH}/DailyNotes/ --files-with-matches)

## Key Notes

## Next Week Goals
- [ ]
"
```

---

## Obsidian URI Workflows

### Quick Capture

```bash
# Quick note capture
TITLE="Quick Note $(date +%H:%M)"
CONTENT="Captured at $(date)"

open "obsidian://new?vault=${OBSIDIAN_VAULT_NAME}&name=${TITLE}&content=${CONTENT}"
```

### Open Today's Daily Note

```bash
# Using Obsidian's daily note command
open "obsidian://advanced-uri?vault=${OBSIDIAN_VAULT_NAME}&daily=true"
```

### Search and Open

```bash
# Search for a term and open in Obsidian
SEARCH_TERM="API design"
open "obsidian://search?vault=${OBSIDIAN_VAULT_NAME}&query=${SEARCH_TERM}"
```

---

## Tips for Complex Workflows

### 1. Combine Tools

Use Grep to find → Read to extract → Edit to modify → Open to verify

### 2. Use Scripts

For complex batch operations, create shell scripts that combine multiple Claude Code tools.

### 3. Preserve Structure

Always read before editing to preserve:
- YAML frontmatter
- Existing tags
- Wikilinks
- Formatting

### 4. Version Control

Consider keeping your vault in git for:
- Change tracking
- Rollback capability
- Collaboration

```bash
cd ${OBSIDIAN_VAULT_PATH}
git add -A
git commit -m "Batch update: added #AI tags"
```

---

## See Also

- [README.md](./README.md) - Setup and basic usage
- [Obsidian URI Documentation](https://help.obsidian.md/Extending+Obsidian/Obsidian+URI)
- [Obsidian Markdown Reference](https://help.obsidian.md/Editing+and+formatting/Obsidian+Flavored+Markdown)
