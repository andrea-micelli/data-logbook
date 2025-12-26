from constants import COLOR_GREEN, COLOR_RED, COLOR_RESET
from init import ENTRY_FILENAME
import os
from datetime import datetime
import sys
import subprocess


# --- UTILITY FUNCTIONS (Updated for selection) ---

def open_folder_in_explorer(path, select_file=None):
    """
    Opens the specified folder path in the system's file explorer.
    If select_file is provided, attempts to highlight that file within the folder.
    """
    if not os.path.exists(path):
        print(f"\n{COLOR_RED}[Error] Target path not found at: {path}{COLOR_RESET}")
        return

    try:
        if select_file and os.path.exists(select_file):
            if sys.platform == "win32":
                # Windows: uses /select argument to highlight a file
                subprocess.Popen(['explorer', '/select,', os.path.abspath(select_file)])
                print(f"{COLOR_GREEN}Opened folder and selected file: {select_file}{COLOR_RESET}")
                return
            elif sys.platform == "darwin":
                # macOS: uses 'select' argument with 'open'
                subprocess.Popen(['open', '-R', os.path.abspath(select_file)])
                print(f"{COLOR_GREEN}Opened folder and selected file: {select_file}{COLOR_RESET}")
                return
        
        # Default behavior (if no file to select or OS not explicitly handled for selection)
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(['open', path])
        else:
            # Linux (using xdg-open)
            subprocess.Popen(['xdg-open', path])
        
        print(f"{COLOR_GREEN}Opened folder: {path}{COLOR_RESET}")
    except Exception as e:
        print(f"\n{COLOR_RED}[Error] Could not open folder. Command failed: {e}{COLOR_RESET}")


def format_timestamp(ts):
    """Converts a datetime object or string back into a readable date string."""
    if isinstance(ts, datetime):
        return ts.strftime("%d-%m-%Y")
    return str(ts)


def print_help():
    print( "\n--- Available Commands ---")
    print(f"{COLOR_GREEN}new{COLOR_RESET}                   : Create a new logbook entry (creates folder and {ENTRY_FILENAME}).")
    print(f"{COLOR_GREEN}list{COLOR_RESET}                  : Display the chronological list of entries.")
    print(f"{COLOR_GREEN}show <N>{COLOR_RESET}              : Select an entry to view metadata and raw Markdown.")
    print(f"{COLOR_GREEN}open <N>{COLOR_RESET}              : Open the entry's folder in file explorer and select the {ENTRY_FILENAME} file.")
    print(f"{COLOR_GREEN}edit <N>{COLOR_RESET}              : Open the log_entry.md file in the default editor.")
    print(f"{COLOR_GREEN}search <field> <text>{COLOR_RESET} : Add filter.")
    print(f"{COLOR_GREEN}reset{COLOR_RESET}                 : Reset filters.")
    print(f"{COLOR_GREEN}help <command>                     : Prints instructions on how to use the command.{COLOR_RESET}")
    print(f"{COLOR_GREEN}quit (or exit){COLOR_RESET}        : Exit the application.")
    print( "--------------------------")


def print_help_command(command):
    match command:
        case 'new':
            print(f"{COLOR_GREEN}new{COLOR_RESET}")
            print("Create a new logbook entry.")
            print("- Prompts for metadata and creates a new folder under the logbook root.")
            print(f"- Generates a fresh {ENTRY_FILENAME} Markdown file inside that folder.")        
        case 'list':
            print(f"{COLOR_GREEN}list{COLOR_RESET}")
            print("Show the chronological list of entries, with their index numbers.")
            print("- Use the index N with other commands such as show, open, edit.")
            print("- Honors any active search filters.")
        case 'show':
            print(f"{COLOR_GREEN}show <N>{COLOR_RESET}")
            print("Display details for entry N.")
            print("- Shows stored metadata for the selected entry.")
            print(f"- Prints the raw contents of the {ENTRY_FILENAME} file to the terminal.")
        case 'open':
            print(f"{COLOR_GREEN}open <N>{COLOR_RESET}")
            print("Open the folder of entry N in the file explorer.")
            print(f"- Selects the {ENTRY_FILENAME} file inside the entry folder.")
            print("- Useful when you want to manage attachments or other files manually.")
        case 'edit':
            print(f"{COLOR_GREEN}edit <N>{COLOR_RESET}")
            print(f"Open the {ENTRY_FILENAME} of entry N in the default editor.")
            print("- Uses the OS default application for Markdown files (or text files).")
            print("- Save and close the editor to keep changes in the logbook.")
        case 'search':
            print(f"{COLOR_GREEN}search <field> <text>{COLOR_RESET}")
            print("Add a filter to narrow down entries in list/show operations.")
            print("- <field> is one of the searchable metadata fields (e.g. date, tag, title).")
            print("- <text> is matched against the chosen field (usually case-insensitive).")
        case 'reset':
            print(f"{COLOR_GREEN}reset{COLOR_RESET}")
            print("Clear all active search filters.")
            print("- After reset, list and show operate on the full set of entries again.")
        case 'quit' | 'exit':
            print(f"{COLOR_GREEN}quit{COLOR_RESET} / {COLOR_GREEN}exit{COLOR_RESET}")
            print("Terminate the application.")
            print("- Any saved entries remain on disk.")
            print("- Unsaved edits in external editors are not managed by the logbook.")
        case 'help':
            print(f"{COLOR_GREEN}help [command]{COLOR_RESET}")
            print("Show general help or detailed help for a specific command.")
            print("- Run `help` to see the list of all commands.")
            print("- Run `help <command>` for usage notes on that command.")
        case _:
            print(f'"{command}" is not a known command. Type "help" to see available commands.')
