#!/usr/bin/env python3
"""
macOS Notes Manager - Manipulate Apple Notes via AppleScript

This script provides a Python interface to Apple Notes using AppleScript.
It supports listing, creating, reading, searching, and deleting notes.

IMPORTANT: Apple Notes organizes notes by ACCOUNT (iCloud, On My Mac, Gmail, etc.)
This script queries ALL accounts by default.

Usage:
    python notes_manager.py <command> [options]

Commands:
    list-accounts             List all accounts
    list-folders              List all folders (across all accounts)
    list-notes [--folder] [--account]  List notes
    create --title --body [--folder] [--account]  Create a new note
    read --title [--folder]   Read note content by title
    search --query            Search notes by content
    delete --title [--folder] Delete a note by title

Requirements:
    - macOS with Notes.app
    - First run will prompt for Automation permission
"""

import subprocess
import json
import sys
import argparse
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


def list_accounts() -> dict:
    """List all accounts in Notes (iCloud, On My Mac, etc.)."""
    script = '''
    tell application "Notes"
        set accountList to ""
        repeat with a in accounts
            set accountList to accountList & name of a & linefeed
        end repeat
        return accountList
    end tell
    '''
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    # Parse newline-separated list
    accounts = [line.strip() for line in output.split("\n") if line.strip()]
    
    return {"success": True, "accounts": accounts, "count": len(accounts)}


def list_folders() -> dict:
    """List all folders across all accounts."""
    script = '''
    tell application "Notes"
        set folderList to ""
        repeat with a in accounts
            set accountName to name of a
            repeat with f in folders of a
                set folderList to folderList & accountName & " > " & name of f & " (" & (count of notes in f) & " notes)" & linefeed
            end repeat
        end repeat
        return folderList
    end tell
    '''
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    # Parse newline-separated list
    folders = [line.strip() for line in output.split("\n") if line.strip()]
    
    return {"success": True, "folders": folders, "count": len(folders)}


def list_notes(folder: Optional[str] = None, account: Optional[str] = None) -> dict:
    """List all notes across all accounts, optionally filtered."""
    
    if account and folder:
        escaped_account = escape_for_applescript(account)
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            set noteList to ""
            try
                set targetAccount to account "{escaped_account}"
                set targetFolder to folder "{escaped_folder}" of targetAccount
                repeat with n in notes of targetFolder
                    set noteList to noteList & name of n & linefeed
                end repeat
            on error errMsg
                return "ERROR: " & errMsg
            end try
            return noteList
        end tell
        '''
    elif account:
        escaped_account = escape_for_applescript(account)
        script = f'''
        tell application "Notes"
            set noteList to ""
            try
                set targetAccount to account "{escaped_account}"
                repeat with n in notes of targetAccount
                    set noteList to noteList & name of n & linefeed
                end repeat
            on error errMsg
                return "ERROR: " & errMsg
            end try
            return noteList
        end tell
        '''
    elif folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            set noteList to ""
            repeat with a in accounts
                try
                    set targetFolder to folder "{escaped_folder}" of a
                    repeat with n in notes of targetFolder
                        set noteList to noteList & (name of a) & " > " & name of n & linefeed
                    end repeat
                end try
            end repeat
            return noteList
        end tell
        '''
    else:
        # List ALL notes from ALL accounts - use linefeed as delimiter
        script = '''
        tell application "Notes"
            set noteList to ""
            repeat with a in accounts
                set accountName to name of a
                repeat with n in notes of a
                    set noteList to noteList & accountName & " > " & name of n & linefeed
                end repeat
            end repeat
            return noteList
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    # Parse newline-separated list (much more reliable than comma parsing)
    notes = [line.strip() for line in output.split("\n") if line.strip()]
    
    return {"success": True, "notes": notes, "count": len(notes)}


def create_note(title: str, body: str, folder: Optional[str] = None, account: Optional[str] = None) -> dict:
    """Create a new note."""
    escaped_title = escape_for_applescript(title)
    escaped_body = escape_for_applescript(body)
    
    if account and folder:
        escaped_account = escape_for_applescript(account)
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to account "{escaped_account}"
                set targetFolder to folder "{escaped_folder}" of targetAccount
                set newNote to make new note at targetFolder with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                return "SUCCESS: Created note '" & name of newNote & "'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    elif account:
        escaped_account = escape_for_applescript(account)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to account "{escaped_account}"
                set defaultFolder to default folder of targetAccount
                set newNote to make new note at defaultFolder with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                return "SUCCESS: Created note '" & name of newNote & "'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    elif folder:
        escaped_folder = escape_for_applescript(folder)
        script = f'''
        tell application "Notes"
            try
                -- Find folder in any account
                repeat with a in accounts
                    try
                        set targetFolder to folder "{escaped_folder}" of a
                        set newNote to make new note at targetFolder with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                        return "SUCCESS: Created note '" & name of newNote & "' in " & name of a
                    end try
                end repeat
                return "ERROR: Folder not found"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        # Create in default folder of first account (usually iCloud)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to first account
                set defaultFolder to default folder of targetAccount
                set newNote to make new note at defaultFolder with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
                return "SUCCESS: Created note '" & name of newNote & "' in " & name of targetAccount
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


def read_note(title: str, folder: Optional[str] = None, account: Optional[str] = None, plaintext: bool = False) -> dict:
    """Read a note's content by title, searching all accounts."""
    escaped_title = escape_for_applescript(title)
    content_property = "plaintext" if plaintext else "body"
    
    if account:
        escaped_account = escape_for_applescript(account)
        if folder:
            escaped_folder = escape_for_applescript(folder)
            script = f'''
            tell application "Notes"
                try
                    set targetAccount to account "{escaped_account}"
                    set targetFolder to folder "{escaped_folder}" of targetAccount
                    set targetNote to first note of targetFolder whose name is "{escaped_title}"
                    return {content_property} of targetNote
                on error errMsg
                    return "ERROR: " & errMsg
                end try
            end tell
            '''
        else:
            script = f'''
            tell application "Notes"
                try
                    set targetAccount to account "{escaped_account}"
                    set targetNote to first note of targetAccount whose name is "{escaped_title}"
                    return {content_property} of targetNote
                on error errMsg
                    return "ERROR: " & errMsg
                end try
            end tell
            '''
    else:
        # Search all accounts
        script = f'''
        tell application "Notes"
            repeat with a in accounts
                try
                    set targetNote to first note of a whose name is "{escaped_title}"
                    return {content_property} of targetNote
                end try
            end repeat
            return "ERROR: Note not found"
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "title": title, "content": output, "format": "plaintext" if plaintext else "html"}


def search_notes(query: str) -> dict:
    """Search notes by content across all accounts."""
    escaped_query = escape_for_applescript(query.lower())
    
    script = f'''
    tell application "Notes"
        set matchingNotes to ""
        set searchQuery to "{escaped_query}"
        repeat with a in accounts
            set accountName to name of a
            repeat with n in notes of a
                try
                    set noteName to name of n
                    set noteBody to plaintext of n
                    set lowerName to do shell script "echo " & quoted form of noteName & " | tr '[:upper:]' '[:lower:]'"
                    set lowerBody to do shell script "echo " & quoted form of noteBody & " | tr '[:upper:]' '[:lower:]'"
                    if (lowerBody contains searchQuery) or (lowerName contains searchQuery) then
                        set matchingNotes to matchingNotes & accountName & " > " & noteName & linefeed
                    end if
                end try
            end repeat
        end repeat
        return matchingNotes
    end tell
    '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    # Parse newline-separated list
    notes = [line.strip() for line in output.split("\n") if line.strip()]
    
    return {"success": True, "query": query, "notes": notes, "count": len(notes)}


def delete_note(title: str, folder: Optional[str] = None, account: Optional[str] = None) -> dict:
    """Delete a note by title."""
    escaped_title = escape_for_applescript(title)
    
    if account:
        escaped_account = escape_for_applescript(account)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to account "{escaped_account}"
                set targetNote to first note of targetAccount whose name is "{escaped_title}"
                delete targetNote
                return "SUCCESS: Deleted note '{title}'"
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        # Search all accounts
        script = f'''
        tell application "Notes"
            repeat with a in accounts
                try
                    set targetNote to first note of a whose name is "{escaped_title}"
                    delete targetNote
                    return "SUCCESS: Deleted note '{title}' from " & name of a
                end try
            end repeat
            return "ERROR: Note not found"
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def create_folder(name: str, account: Optional[str] = None) -> dict:
    """Create a new folder."""
    escaped_name = escape_for_applescript(name)
    
    if account:
        escaped_account = escape_for_applescript(account)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to account "{escaped_account}"
                set newFolder to make new folder at targetAccount with properties {{name:"{escaped_name}"}}
                return "SUCCESS: Created folder '" & name of newFolder & "' in " & name of targetAccount
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
    else:
        script = f'''
        tell application "Notes"
            try
                set targetAccount to first account
                set newFolder to make new folder at targetAccount with properties {{name:"{escaped_name}"}}
                return "SUCCESS: Created folder '" & name of newFolder & "' in " & name of targetAccount
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


def append_to_note(title: str, text: str, account: Optional[str] = None) -> dict:
    """Append text to an existing note."""
    escaped_title = escape_for_applescript(title)
    escaped_text = escape_for_applescript(text)
    
    if account:
        escaped_account = escape_for_applescript(account)
        script = f'''
        tell application "Notes"
            try
                set targetAccount to account "{escaped_account}"
                set targetNote to first note of targetAccount whose name is "{escaped_title}"
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
            repeat with a in accounts
                try
                    set targetNote to first note of a whose name is "{escaped_title}"
                    set currentBody to body of targetNote
                    set body of targetNote to currentBody & "<br>" & "{escaped_text}"
                    return "SUCCESS: Appended to note '{title}' in " & name of a
                end try
            end repeat
            return "ERROR: Note not found"
        end tell
        '''
    
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    if output.startswith("ERROR:"):
        return {"success": False, "error": output}
    
    return {"success": True, "message": output}


def get_note_count() -> dict:
    """Get total note count across all accounts (diagnostic)."""
    script = '''
    tell application "Notes"
        set totalCount to 0
        set accountInfo to {}
        repeat with a in accounts
            set accountName to name of a
            set noteCount to count of notes of a
            set totalCount to totalCount + noteCount
            set end of accountInfo to accountName & ": " & noteCount & " notes"
        end repeat
        return (totalCount as string) & " total | " & (accountInfo as string)
    end tell
    '''
    success, output = run_applescript(script)
    
    if not success:
        return {"success": False, "error": output}
    
    return {"success": True, "info": output}


def main():
    parser = argparse.ArgumentParser(
        description="Manage Apple Notes from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # list-accounts command
    subparsers.add_parser("list-accounts", help="List all accounts (iCloud, On My Mac, etc.)")
    
    # list-folders command
    subparsers.add_parser("list-folders", help="List all folders")
    
    # list-notes command
    list_parser = subparsers.add_parser("list-notes", help="List notes")
    list_parser.add_argument("--folder", "-f", help="Filter by folder name")
    list_parser.add_argument("--account", "-a", help="Filter by account (e.g., 'iCloud')")
    
    # create command
    create_parser = subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("--title", "-t", required=True, help="Note title")
    create_parser.add_argument("--body", "-b", required=True, help="Note body content")
    create_parser.add_argument("--folder", "-f", help="Target folder")
    create_parser.add_argument("--account", "-a", help="Target account (e.g., 'iCloud')")
    
    # read command
    read_parser = subparsers.add_parser("read", help="Read a note")
    read_parser.add_argument("--title", "-t", required=True, help="Note title")
    read_parser.add_argument("--folder", "-f", help="Folder to search in")
    read_parser.add_argument("--account", "-a", help="Account to search in")
    read_parser.add_argument("--plaintext", "-p", action="store_true", help="Get plaintext instead of HTML")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("--query", "-q", required=True, help="Search query")
    
    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a note")
    delete_parser.add_argument("--title", "-t", required=True, help="Note title")
    delete_parser.add_argument("--folder", "-f", help="Folder to search in")
    delete_parser.add_argument("--account", "-a", help="Account to search in")
    
    # create-folder command
    folder_parser = subparsers.add_parser("create-folder", help="Create a new folder")
    folder_parser.add_argument("--name", "-n", required=True, help="Folder name")
    folder_parser.add_argument("--account", "-a", help="Target account")
    
    # append command
    append_parser = subparsers.add_parser("append", help="Append text to a note")
    append_parser.add_argument("--title", "-t", required=True, help="Note title")
    append_parser.add_argument("--text", required=True, help="Text to append")
    append_parser.add_argument("--account", "-a", help="Account to search in")
    
    # diagnostic command
    subparsers.add_parser("count", help="Get note count per account (diagnostic)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "list-accounts":
        result = list_accounts()
    elif args.command == "list-folders":
        result = list_folders()
    elif args.command == "list-notes":
        result = list_notes(args.folder, getattr(args, 'account', None))
    elif args.command == "create":
        result = create_note(args.title, args.body, args.folder, getattr(args, 'account', None))
    elif args.command == "read":
        result = read_note(args.title, args.folder, getattr(args, 'account', None), args.plaintext)
    elif args.command == "search":
        result = search_notes(args.query)
    elif args.command == "delete":
        result = delete_note(args.title, args.folder, getattr(args, 'account', None))
    elif args.command == "create-folder":
        result = create_folder(args.name, getattr(args, 'account', None))
    elif args.command == "append":
        result = append_to_note(args.title, args.text, getattr(args, 'account', None))
    elif args.command == "count":
        result = get_note_count()
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
