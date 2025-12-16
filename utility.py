from constants import COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_RESET, ENTRY_FILENAME, FRONT_MATTER_DELIMITER # noqa: F401
import os # noqa: F401
from datetime import datetime # noqa: F401
import sys # noqa: F401
import subprocess # noqa: F401


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