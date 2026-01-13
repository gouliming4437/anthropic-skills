---
name: macos-notes
description: Manage Apple Notes on macOS via AppleScript. Use when the user wants to create, read, list, search, delete, or organize notes in Apple Notes.app. Supports folder management, note creation with rich text, searching by content, and reading notes as HTML or plaintext. Requires macOS with Notes.app and Automation permission.
---

# macOS Notes Manager

Manipulate Apple Notes using AppleScript via Python.

## Quick Start

This skill runs in the user's miniconda `pytest` environment:

```bash
conda activate pytest
```

Run the script with Python:

```bash
python3 scripts/notes_manager.py <command> [options]
```

## Available Commands

### List Folders
```bash
python3 scripts/notes_manager.py list-folders
```

### List Notes
```bash
# All notes
python3 scripts/notes_manager.py list-notes

# Notes in specific folder
python3 scripts/notes_manager.py list-notes --folder "Work"
```

### Create Note
```bash
python3 scripts/notes_manager.py create --title "Meeting Notes" --body "Discussion points..."

# In specific folder
python3 scripts/notes_manager.py create --title "Meeting Notes" --body "Content" --folder "Work"
```

### Read Note
```bash
# Returns HTML content
python3 scripts/notes_manager.py read --title "Meeting Notes"

# Returns plaintext
python3 scripts/notes_manager.py read --title "Meeting Notes" --plaintext
```

### Search Notes
```bash
python3 scripts/notes_manager.py search --query "project deadline"
```

### Delete Note
```bash
python3 scripts/notes_manager.py delete --title "Old Note"
```

### Create Folder
```bash
python3 scripts/notes_manager.py create-folder --name "Projects"
```

### Append to Note
```bash
python3 scripts/notes_manager.py append --title "Daily Log" --text "New entry..."
```

## Output Format

All commands return JSON:
```json
{
  "success": true,
  "notes": [...],
  "message": "..."
}
```

## Permissions

First run will trigger macOS Automation permission dialog. Grant access to allow script to control Notes.app.

## Limitations

- Rich text formatting (bold, lists, etc.) requires HTML in body
- Attachments and images are not supported
- iCloud-synced notes may have slight delays
- Note titles must be unique within a folder for reliable read/delete

## HTML Formatting Examples

Create formatted notes using HTML:

```bash
python3 scripts/notes_manager.py create --title "Formatted Note" --body "<h1>Header</h1><p>Paragraph with <b>bold</b> and <i>italic</i>.</p><ul><li>Item 1</li><li>Item 2</li></ul>"
```
