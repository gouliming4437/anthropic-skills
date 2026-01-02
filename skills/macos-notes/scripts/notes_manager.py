#!/usr/bin/env python3
"""
macOS Notes Manager - Manipulate Apple Notes via AppleScript

This script provides a Python interface to Apple Notes using AppleScript.
It supports listing, creating, reading, searching, and deleting notes.

Usage:
    python notes_manager.py <command> [options]

Commands:
    list-folders              List all folders
    list-notes [--folder]     List notes (optionally filter by folder)
    create --title --body [--folder]  Create a new note
    read --title [--folder]   Read note content by title
    search --query            Search notes by content
    delete --title [--folder] Delete a note by title
    export --title [--folder] [--format]  Export note to file

Requirements:
    - macOS with Notes.app
    - First run will prompt for Automation permission
"""

import subprocess
import json
import sys
import argparse
import html
from datetime import datetime
from typing import Optional


def run_applescript(script: str) -> tuple[bool, str]:
    """Execute AppleScript and return (success, output)."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "AppleScript execution timed out"
    except Exception as e:
        return False, str(e)


def escape_for_applescript(text: str) -> str:
    """Escape text for use in AppleScript strings."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def list_folders() -> dict:
    """List all folders in Notes."""
    script = '''
    tell application "Notes"
        set folderList to {}
        repeat with f in folders
            set folderInfo to {name of f, id of f, (count of notes in f)}
            set end of folderList to folderInfo
        end repeat
        return folderList
    end tell
    '''
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    # Parse the AppleScript list output
    folders = []
    if output:
        # AppleScript returns: {{name, id, count}, {name, id, count}, ...}
        # We need to parse this format
        try:
            # Simple parsing for the expected format
            items = output.strip()
            if items.startswith("{{") and items.endswith("}}"):
                # Multiple folders
                items = items[1:-1]  # Remove outer braces
                # Split by "}, {" to get individual folder entries
                folder_strings = items.split("}, {")
                for fs in folder_strings:
                    fs = fs.strip("{}")
                    parts = fs.split(", ")
                    if len(parts) >= 3:
                        name = parts[0].strip()
                        count = int(parts[-1]) if parts[-1].isdigit() else 0
                        folders.append({"name": name, "note_count": count})
            elif items.startswith("{") and items.endswith("}"):
                # Single folder
                parts = items.strip("{}").split(", ")
                if len(parts) >= 3:
                    name = parts[0].strip()
                    count = int(parts[-1]) if parts[-1].isdigit() else 0
                    folders.append({"name": name, "note_count": count})
        except Exception as e:
            # Fallback: return raw output
            return {"success": True, "folders": [], "raw": output}
    
    return {"success": True, "folders": folders}


def list_notes(folder: Optional[str] = None) -> dict:
    """List all notes, optionally filtered by folder."""
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            set noteList to {{}}
            try
                set targetFolder to folder "{escaped_folder}"
                repeat with n in notes of targetFolder
                    set noteInfo to {{name of n, id of n, modification date of n as string}}
                    set end of noteList to noteInfo
                end repeat
            on error errMsg
                return "ERROR: " & errMsg
            end try
            return noteList
        end tell
        '''
    else:
        script = '''
        tell application "Notes"
            set noteList to {}
            repeat with n in notes
                set noteInfo to {name of n, id of n, modification date of n as string}
                set end of noteList to noteInfo
            end repeat
            return noteList
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    notes = []
    if output and output != "{}":
        try:
            # Parse AppleScript list format
            items = output.strip()
            if items.startswith("{{") and items.endswith("}}"):
                items = items[1:-1]
                note_strings = items.split("}, {")
                for ns in note_strings:
                    ns = ns.strip("{}")
                    # Find the last two commas to split correctly (name may contain commas)
                    parts = ns.rsplit(", ", 2)
                    if len(parts) >= 1:
                        name = parts[0].strip()
                        mod_date = parts[-1] if len(parts) > 1 else ""
                        notes.append({"title": name, "modified": mod_date})
            elif items.startswith("{") and items.endswith("}"):
                parts = items.strip("{}").rsplit(", ", 2)
                if len(parts) >= 1:
                    name = parts[0].strip()
                    mod_date = parts[-1] if len(parts) > 1 else ""
                    notes.append({"title": name, "modified": mod_date})
        except Exception as e:
            return {"success": True, "notes": [], "raw": output}
    
    return {"success": True, "notes": notes, "count": len(notes)}


def create_note(title: str, body: str, folder: Optional[str] = None) -> dict:
    """Create a new note."""
    escaped_title = escape_for_applescript(title)
    escaped_body = escape_for_applescript(body)
    
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetFolder to folder "{escaped_folder}"
                set newNote to make new note at targetFolder with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                return "SUCCESS: Created note '" & name of newNote & "' in folder '{folder}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set newNote to make new note with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                return "SUCCESS: Created note '" & name of newNote & "'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def read_note(title: str, folder: Optional[str] = None) -> dict:
    """Read a note's content by title."""
    escaped_title = escape_for_applescript(title)
    
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetFolder to folder "{escaped_folder}"
                set targetNote to first note of targetFolder whose name is "{escaped_title}"
                set noteBody to body of targetNote
                return noteBody
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set targetNote to first note whose name is "{escaped_title}"
                set noteBody to body of targetNote
                return noteBody
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    # Notes returns HTML-formatted content
    return {"success": True, "title": title, "content": output, "format": "html"}


def search_notes(query: str) -> dict:
    """Search notes by content (case-insensitive)."""
    escaped_query = escape_for_applescript(query.lower())
    
    script = f'''
    tell application "Notes"
        set matchingNotes to {{}}
        set searchQuery to "{escaped_query}"
        repeat with n in notes
            try
                set noteName to name of n
                set noteBody to plaintext of n
                if (noteBody contains searchQuery) or (noteName contains searchQuery) then
                    set noteInfo to {{noteName, modification date of n as string}}
                    set end of matchingNotes to noteInfo
                end if
            end try
        end repeat
        return matchingNotes
    end tell
    '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    notes = []
    if output and output != "{}":
        try:
            items = output.strip()
            if items.startswith("{{") and items.endswith("}}"):
                items = items[1:-1]
                note_strings = items.split("}, {")
                for ns in note_strings:
                    ns = ns.strip("{}")
                    parts = ns.rsplit(", ", 1)
                    if len(parts) >= 1:
                        name = parts[0].strip()
                        mod_date = parts[-1] if len(parts) > 1 else ""
                        notes.append({"title": name, "modified": mod_date})
            elif items.startswith("{") and items.endswith("}"):
                parts = items.strip("{}").rsplit(", ", 1)
                if len(parts) >= 1:
                    name = parts[0].strip()
                    mod_date = parts[-1] if len(parts) > 1 else ""
                    notes.append({"title": name, "modified": mod_date})
        except Exception:
            return {"success": True, "notes": [], "raw": output}
    
    return {"success": True, "query": query, "notes": notes, "count": len(notes)}


def delete_note(title: str, folder: Optional[str] = None) -> dict:
    """Delete a note by title."""
    escaped_title = escape_for_applescript(title)
    
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetFolder to folder "{escaped_folder}"
                set targetNote to first note of targetFolder whose name is "{escaped_title}"
                delete targetNote
                return "SUCCESS: Deleted note '{title}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set targetNote to first note whose name is "{escaped_title}"
                delete targetNote
                return "SUCCESS: Deleted note '{title}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def get_note_plaintext(title: str, folder: Optional[str] = None) -> dict:
    """Get a note's content as plain text."""
    escaped_title = escape_for_applescript(title)
    
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetFolder to folder "{escaped_folder}"
                set targetNote to first note of targetFolder whose name is "{escaped_title}"
                set noteContent to plaintext of targetNote
                return noteContent
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set targetNote to first note whose name is "{escaped_title}"
                set noteContent to plaintext of targetNote
                return noteContent
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "title": title, "content": output, "format": "plaintext"}


def create_folder(name: str) -> dict:
    """Create a new folder in Notes."""
    escaped_name = escape_for_applescript(name)
    
    script = f'''
    tell application "Notes"
        try
            set newFolder to make new folder with properties {{name:"{escaped_name}"}}
            return "SUCCESS: Created folder '" & name of newFolder & "'"
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def append_to_note(title: str, text: str, folder: Optional[str] = None) -> dict:
    """Append text to an existing note."""
    escaped_title = escape_for_applescript(title)
    escaped_text = escape_for_applescript(text)
    
    if folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetFolder to folder "{escaped_folder}"
                set targetNote to first note of targetFolder whose name is "{escaped_title}"
                set currentBody to body of targetNote
                set body of targetNote to currentBody & "<br>" & "{escaped_text}"
                return "SUCCESS: Appended to note '{title}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set targetNote to first note whose name is "{escaped_title}"
                set currentBody to body of targetNote
                set body of targetNote to currentBody & "<br>" & "{escaped_text}"
                return "SUCCESS: Appended to note '{title}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def main():
    parser = argparse.ArgumentParser(
        description="Manage Apple Notes from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # list-folders command
    subparsers.add_parser("list-folders", help="List all folders")
    
    # list-notes command
    list_parser = subparsers.add_parser("list-notes", help="List notes")
    list_parser.add_argument("--folder", "-f", help="Filter by folder name")
    
    # create command
    create_parser = subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("--title", "-t", required=True, help="Note title")
    create_parser.add_argument("--body", "-b", required=True, help="Note body content")
    create_parser.add_argument("--folder", "-f", help="Target folder")
    
    # read command
    read_parser = subparsers.add_parser("read", help="Read a note")
    read_parser.add_argument("--title", "-t", required=True, help="Note title")
    read_parser.add_argument("--folder", "-f", help="Folder to search in")
    read_parser.add_argument("--plaintext", "-p", action="store_true", help="Get plaintext instead of HTML")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("--query", "-q", required=True, help="Search query")
    
    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("--title", "-t", required=True, help="Note title")
    delete_parser.add_argument("--folder", "-f", help="Folder to search in")
    
    # create-folder command
    folder_parser = subparsers.add_parser("create-folder", help="Create a new folder")
    folder_parser.add_argument("--name", "-n", required=True, help="Folder name")
    
    # append command
    append_parser = subparsers.add_parser("append", help="Append text to a note")
    append_parser.add_argument("--title", "-t", required=True, help="Note title")
    append_parser.add_argument("--text", required=True, help="Text to append")
    append_parser.add_argument("--folder", "-f", help="Folder to search in")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "list-folders":
        result = list_folders()
    elif args.command == "list-notes":
        result = list_notes(args.folder)
    elif args.command == "create":
        result = create_note(args.title, args.body, args.folder)
    elif args.command == "read":
        if args.plaintext:
            result = get_note_plaintext(args.title, args.folder)
        else:
            result = read_note(args.title, args.folder)
    elif args.command == "search":
        result = search_notes(args.query)
    elif args.command == "delete":
        result = delete_note(args.title, args.folder)
    elif args.command == "create-folder":
        result = create_folder(args.name)
    elif args.command == "append":
        result = append_to_note(args.title, args.text, args.folder)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Output as JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Exit with error code if operation failed
    if not result.get("success", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
