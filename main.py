import yaml
import os
import subprocess
from datetime import datetime
import sys
import shutil 

# --- ANSI COLOR CODES ---
COLOR_BLUE = '\033[94m'    # Headers, Titles
COLOR_GREEN = '\033[92m'   # Success Messages, Commands
COLOR_YELLOW = '\033[93m'  # Prompts, User Input Fields, Hints
COLOR_RED = '\033[91m'     # Errors, Warnings
COLOR_RESET = '\033[0m'    # Reset color

# --- CONFIGURATION ---
ENTRY_FILENAME = 'log_entry.md'
DEFAULT_DATA_FOLDER_ROOT = 'data' 
FRONT_MATTER_DELIMITER = '---'

# --- DATA MANAGEMENT FUNCTIONS (Unchanged) ---

def parse_markdown_entry(content):
    """
    Parses a Markdown file content string expecting YAML Front Matter.
    Returns a tuple: (metadata_dict, markdown_body)
    """
    parts = content.split(FRONT_MATTER_DELIMITER, 2)
    
    if len(parts) < 3:
        return {"title": "Error: Invalid Format", "timestamp": "N/A"}, content

    yaml_block = parts[1].strip()
    markdown_body = parts[2].strip()

    try:
        metadata = yaml.safe_load(yaml_block)
        if not isinstance(metadata, dict):
             raise yaml.YAMLError("YAML front matter is not a dictionary.")
        return metadata, markdown_body
    except yaml.YAMLError:
        return {"title": "Error: YAML Parse Fail", "timestamp": "N/A"}, content


def load_entries():
    """Scans the DEFAULT_DATA_FOLDER_ROOT for entry directories and loads their metadata."""
    entries = []
    
    if not os.path.exists(DEFAULT_DATA_FOLDER_ROOT):
        print(f"{COLOR_YELLOW}Data directory '{DEFAULT_DATA_FOLDER_ROOT}' not found. No entries loaded.{COLOR_RESET}")
        os.makedirs(DEFAULT_DATA_FOLDER_ROOT, exist_ok=True)
        return []

    for item_name in os.listdir(DEFAULT_DATA_FOLDER_ROOT):
        entry_folder_path = os.path.join(DEFAULT_DATA_FOLDER_ROOT, item_name)
        entry_file_path = os.path.join(entry_folder_path, ENTRY_FILENAME)

        if os.path.isdir(entry_folder_path) and os.path.exists(entry_file_path):
            try:
                with open(entry_file_path, 'r') as f:
                    content = f.read()
                
                metadata, description = parse_markdown_entry(content)
                
                if 'title' in metadata and 'timestamp' in metadata:
                    entry = metadata
                    entry['description'] = description
                    entry['data_folder'] = entry_folder_path
                    entries.append(entry)
                else:
                    print(f"{COLOR_RED}Warning: Skipping {entry_file_path} (missing title/timestamp in metadata).{COLOR_RESET}")

            except Exception as e:
                print(f"{COLOR_RED}Unexpected error loading entry {entry_folder_path}: {e}{COLOR_RESET}")

    entries.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
    return entries

def save_entry_metadata(entry, description_body):
    """Saves the entry's metadata and description body into its entry_filename file."""
    if 'data_folder' not in entry:
        print(f"{COLOR_RED}[Error] Cannot save entry: missing 'data_folder' path.{COLOR_RESET}")
        return

    entry_file_path = os.path.join(entry['data_folder'], ENTRY_FILENAME)
    
    try:
        os.makedirs(entry['data_folder'], exist_ok=True)

        save_metadata = {k: v for k, v in entry.items() if k not in ['description', 'data_folder']}
        
        yaml_front_matter = f"{FRONT_MATTER_DELIMITER}\n"
        yaml_front_matter += yaml.dump(save_metadata, default_flow_style=False)
        yaml_front_matter += f"{FRONT_MATTER_DELIMITER}\n\n"

        full_content = yaml_front_matter + description_body.strip() + "\n"
        
        with open(entry_file_path, 'w') as f:
            f.write(full_content)
            
        print(f"{COLOR_GREEN}Entry saved to: {entry_file_path}{COLOR_RESET}")
    except IOError as e:
        print(f"{COLOR_RED}Error writing entry file {entry_file_path}: {e}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_RED}An unexpected error occurred during saving: {e}{COLOR_RESET}")

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
        return ts.strftime("%Y-%m-%d %H:%M:%S")
    return str(ts)


# --- INTERACTION FUNCTIONS (Updated view_entry) ---

def list_entries(entries):
    """Displays a numbered, chronological list of all entries (title and date)."""
    if not entries:
        print(f"\n{COLOR_YELLOW}--- Logbook is Empty ---")
        print(f"No entries recorded yet. Use 'new' to create an entry.{COLOR_RESET}")
        return False

    sorted_entries = entries 

    print(f"\n{COLOR_BLUE}--- Measurement Logbook (Chronological) ---")
    print(f"No. | Date/Time          | Title")
    print(f"-----------------------------------------------------------------{COLOR_RESET}")
    for i, entry in enumerate(sorted_entries):
        index = i + 1
        date_str = format_timestamp(entry.get('timestamp'))
        title = entry.get('title', 'NO TITLE')
        print(f"{index:<3} | {date_str:<18} | {COLOR_BLUE}{title[:45]:<45}{COLOR_RESET}")

    return sorted_entries

def view_entry(choice_index, entries_list):
    """
    Displays full details of the entry at choice_index.
    Removed deletion prompt.
    """
    if 0 <= choice_index < len(entries_list):
        selected_entry = entries_list[choice_index]

        print(f"\n{COLOR_BLUE}=============================================")
        print(f"Title:       {selected_entry.get('title')}")
        print(f"Timestamp:   {format_timestamp(selected_entry.get('timestamp'))}")
        print(f"Folder:      {selected_entry.get('data_folder')}")
        print(f"File:        {ENTRY_FILENAME}")
        print(f"============================================={COLOR_RESET}")
        print("\nDescription (Raw Markdown):")
        print(selected_entry.get('description', 'N/A')) 
        print(f"{COLOR_BLUE}============================================={COLOR_RESET}")

        return False # No deletion happened

    else:
        print(f"{COLOR_RED}[Error] Invalid number. Please enter a number shown in the 'list' output.{COLOR_RESET}")
        return False

def open_entry_folder(choice_index, entries_list):
    """
    Opens the entry's folder, selecting the Markdown file.
    """
    if 0 <= choice_index < len(entries_list):
        selected_entry = entries_list[choice_index]
        data_path = selected_entry.get('data_folder')
        file_to_select = os.path.join(data_path, ENTRY_FILENAME)
        
        print(f"\n{COLOR_YELLOW}Attempting to open folder and select {ENTRY_FILENAME} for Entry {choice_index + 1}...{COLOR_RESET}")
        open_folder_in_explorer(data_path, select_file=file_to_select)

    else:
        print(f"{COLOR_RED}[Error] Invalid number. Please enter a number shown in the 'list' output.{COLOR_RESET}")



def open_in_editor(file_path):
    """Open a file in the user's default editor (cross-platform). Blocks until editor closes."""
    import subprocess, sys, os
    try:
        if sys.platform == "win32":
            editor = os.environ.get("EDITOR")
            if editor:
                subprocess.Popen([editor, file_path]).wait()
            else:
                # Try VS Code, else Notepad
                try:
                    subprocess.Popen(["code", file_path]).wait()
                except Exception:
                    subprocess.Popen(["notepad", file_path]).wait()
        elif sys.platform == "darwin":
            editor = os.environ.get("EDITOR")
            if editor:
                subprocess.Popen([editor, file_path]).wait()
            else:
                subprocess.Popen(["open", "-e", file_path]).wait()  # TextEdit
        else:
            editor = os.environ.get("EDITOR", "nano")
            subprocess.Popen([editor, file_path]).wait()
        return True
    except Exception as e:
        print(f"{COLOR_RED}[Error] Could not open editor: {e}{COLOR_RESET}")
        return False


def edit_markdown(choice_index, entries_list):
    """Open the entry's markdown in an external editor; re-parse and normalize after editing."""
    if 0 <= choice_index < len(entries_list):
        entry = entries_list[choice_index]
        md_path = os.path.join(entry['data_folder'], ENTRY_FILENAME)
        if not os.path.exists(md_path):
            print(f"{COLOR_RED}[Error] Markdown file not found: {md_path}{COLOR_RESET}")
            return False
        if open_in_editor(md_path):
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            metadata, description = parse_markdown_entry(content)
            # Preserve data_folder; keep timestamp as-is
            metadata['data_folder'] = entry['data_folder']
            metadata['description'] = description
            save_entry_metadata(metadata, description)
            print(f"{COLOR_GREEN}Markdown updated and metadata normalized.{COLOR_RESET}")
            return True
        return False
    print(f"{COLOR_RED}[Error] Invalid number. Please enter a number shown in the 'list' output.{COLOR_RESET}")
    return False

def edit_entry(choice_index, entries_list):
    """Allows editing the title (metadata) and description (markdown body) of an existing entry."""
    if 0 <= choice_index < len(entries_list):
        selected_entry = entries_list[choice_index]
        current_description = selected_entry.get('description', '')

        print(f"\n{COLOR_BLUE}--- Editing Entry {choice_index + 1}: {selected_entry.get('title')} ---{COLOR_RESET}")

        # 1. Edit Title (Metadata)
        print(f"Current Title: {selected_entry.get('title')}")
        new_title = input(f"{COLOR_YELLOW}Enter new Title (or leave blank to keep current): {COLOR_RESET}").strip()
        if new_title:
            selected_entry['title'] = new_title
            print(f"{COLOR_GREEN}Title updated.{COLOR_RESET}")
        else:
            print("Title unchanged.")

        # 2. Edit Description (Markdown Body)
        print(f"\n{COLOR_BLUE}Current Description (Markdown Body):{COLOR_RESET}")
        print("--------------------------------------------------")
        print(current_description)
        print("--------------------------------------------------")

        print(f"{COLOR_YELLOW}Enter new Description (multi-line input, press Enter on empty line to finish, or 's' to skip editing):{COLOR_RESET}")
        
        new_description_lines = []
        is_editing = True
        while is_editing:
            line = input()
            if not line:
                is_editing = False
            elif line.lower() == 's' and not new_description_lines:
                new_description = current_description
                print("Description unchanged.")
                break
            else:
                new_description_lines.append(line)
        else:
            new_description = '\n'.join(new_description_lines)
            if new_description != current_description:
                 print(f"{COLOR_GREEN}Description updated.{COLOR_RESET}")
            else:
                 print("Description unchanged.")
        
        # 3. Save the changes
        selected_entry['description'] = new_description
        save_entry_metadata(selected_entry, new_description)
        
        return True 

    else:
        print(f"{COLOR_RED}[Error] Invalid number. Please enter a number shown in the 'list' output.{COLOR_RESET}")
        return False


def create_entry(entries):
    """Prompts the user for details and adds a new entry to the list."""
    print(f"\n{COLOR_BLUE}--- Creating New Logbook Entry ---{COLOR_RESET}")

    # 1. Title (Required)
    title = input(f"{COLOR_YELLOW}Enter Title (Required): {COLOR_RESET}").strip()
    while not title:
        print(f"{COLOR_RED}[Error] Title cannot be empty.{COLOR_RESET}")
        title = input(f"{COLOR_YELLOW}Enter Title (Required): {COLOR_RESET}").strip()

    # 2. Description (Markdown Body)
    description = []
    print(f"{COLOR_YELLOW}Enter Description (Markdown body - multi-line input, press Enter on an empty line to finish):{COLOR_RESET}")
    while True:
        line = input()
        if not line:
            break
        description.append(line)
    description = '\n'.join(description)

    # 3. Data Folder Path (Generated from title and timestamp)
    timestamp = datetime.now()
    sanitized_title = title.replace(' ', '_').replace('.', '').replace('/', '').replace('\\', '')
    folder_name = timestamp.strftime("%Y%m%d_%H%M") + "_" + sanitized_title
    data_folder = os.path.join(DEFAULT_DATA_FOLDER_ROOT, folder_name)

    print(f"Data Folder Path: {data_folder}")
    
    # 4. Create the new entry dictionary (metadata)
    new_entry = {
        'timestamp': timestamp,
        'title': title,
        'data_folder': data_folder, 
    }

    # 5. Save metadata/markdown body
    save_entry_metadata(new_entry, description)
    
    # Reload from disk to update the in-memory list
    entries.clear()
    entries.extend(load_entries())
    
# --- MAIN EXECUTION (CLI) ---

def main():
    """Main function to run the logbook application with a command-line interface."""
    
    print(f"{COLOR_BLUE}=============================================")
    print(f"  Lab Measurement Logbook Manager (CLI)")
    print(f"============================================={COLOR_RESET}")
    
    entries = load_entries() 
    
    # Initial list display
    sorted_entries = list_entries(entries)
    
    print(f"\n{COLOR_YELLOW}Enter 'help' for commands, or 'quit' to exit.{COLOR_RESET}")

    while True:
        try:
            cmd_line = input(f"{COLOR_BLUE}logbook> {COLOR_RESET}").strip()
            if not cmd_line:
                continue

            parts = cmd_line.split()
            command = parts[0].lower()
            args = parts[1:]

            if command in ['quit', 'exit']:
                print("\nExiting Logbook Manager. Goodbye!")
                break

            elif command in ['list', 'ls']:
                sorted_entries = list_entries(entries)

            elif command == 'new':
                create_entry(entries)
                sorted_entries = list_entries(entries)

            # New command: open <n>
            elif command == 'open':
                if not args:
                    print(f"{COLOR_RED}[Error] Usage: open <entry_number>{COLOR_RESET}")
                    continue

                try:
                    entry_number = int(args[0])
                    if entries:
                        index = entry_number - 1
                        open_entry_folder(index, entries)
                    else:
                        print(f"{COLOR_RED}[Error] No entries to open.{COLOR_RESET}")
                except ValueError:
                    print(f"{COLOR_RED}[Error] Invalid entry number provided. Must be an integer.{COLOR_RESET}")


            elif command == 'show':
                if not args:
                    print(f"{COLOR_RED}[Error] Usage: show <entry_number>{COLOR_RESET}")
                    continue
                try:
                    entry_number = int(args[0])
                    if entries:
                        index = entry_number - 1
                        view_entry(index, entries)
                    else:
                        print(f"{COLOR_RED}[Error] No entries to show. Use 'new' to create one.{COLOR_RESET}")
                except ValueError:
                    print(f"{COLOR_RED}[Error] Invalid entry number provided. Must be an integer.{COLOR_RESET}")
                        
            elif command == 'edit':
                if not args:
                    print(f"{COLOR_RED}[Error] Usage: edit <entry_number>{COLOR_RESET}")
                    continue
                try:
                    entry_number = int(args[0])
                    if entries:
                        index = entry_number - 1
                        edit_success = edit_markdown(index, entries)
                        if edit_success:
                            entries.clear()
                            entries.extend(load_entries())
                            sorted_entries = list_entries(entries)
                    else:
                        print(f"{COLOR_RED}[Error] No entries to edit. Use 'new' to create one.{COLOR_RESET}")
                except ValueError:
                    print(f"{COLOR_RED}[Error] Invalid entry number provided. Must be an integer.{COLOR_RESET}")
            
            elif command == 'help':
                print(f"\n{COLOR_BLUE}--- Available Commands ---{COLOR_RESET}")
                print(f"{COLOR_GREEN}new{COLOR_RESET}               : Create a new logbook entry (creates folder and {ENTRY_FILENAME}).")
                print(f"{COLOR_GREEN}list (or ls){COLOR_RESET}      : Display the chronological list of entries.")
                print(f"{COLOR_GREEN}sel <number>{COLOR_RESET}      : Select an entry to view metadata and raw Markdown.")
                print(f"{COLOR_GREEN}edit <number>{COLOR_RESET}     : Edit the title and description of an existing entry.")
                print(f"{COLOR_GREEN}open <number>{COLOR_RESET}     : Open the entry's folder in file explorer and select the {ENTRY_FILENAME} file.")
                print(f"{COLOR_GREEN}del <number>{COLOR_RESET}      : Permanently delete the entry and its entire data folder after confirmation.")
                print(f"{COLOR_GREEN}quit (or exit){COLOR_RESET}    : Exit the application.")
                print(f"{COLOR_BLUE}--------------------------{COLOR_RESET}")

            else:
                print(f"{COLOR_RED}[Error] Unknown command: '{command}'. Try 'help'.{COLOR_RESET}")

        except EOFError: 
            print("\nExiting Logbook Manager. Goodbye!")
            break
        except Exception as e:
            print(f"{COLOR_RED}[Fatal Error] An unhandled error occurred: {e}{COLOR_RESET}")
            break

if __name__ == "__main__":
    main()