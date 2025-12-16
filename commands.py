from constants import COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_CYAN, COLOR_RESET, ENTRY_FILENAME, FRONT_MATTER_DELIMITER # noqa: F401
from constants import STYLE_BOLD, STYLE_DIM # noqa: F401
import os
from datetime import datetime
from data_managment import parse_markdown_entry, load_entries, save_entry_metadata
from init import DEFAULT_DATA_FOLDER_ROOT
import sys
import subprocess
from utility import format_timestamp, open_folder_in_explorer


# --- INTERACTION FUNCTIONS (Updated view_entry) ---

def list_entries(entries, filter):
    """Displays a numbered, chronological list of all entries (title and date)."""
    print()  # newline as spacing
    print(f"{COLOR_CYAN}Active filters:{COLOR_RESET}", end=" ")
    if filter:
        for key in filter.keys():
            print(f"{STYLE_BOLD}{key}{COLOR_RESET}={filter[key]}", end="  ")
        print()
    else: 
        print("No active filters")

    if not entries:
        print(f"\n{COLOR_YELLOW}--- Logbook is Empty ---")
        print(f"No entries recorded yet. Use 'new' to create an entry.{COLOR_RESET}")
        return False

    sorted_entries = entries 

    print(f"{COLOR_BLUE}{STYLE_BOLD}{"":-<80}{COLOR_RESET}")
    print(f"{COLOR_BLUE}{STYLE_BOLD} N | {"Date":^10} | Title{COLOR_RESET}")
    print(f"{COLOR_BLUE}{STYLE_BOLD}{"":-<80}{COLOR_RESET}")
    for i, entry in enumerate(sorted_entries):
        index = i + 1
        date_str = format_timestamp(entry.get('timestamp'))
        title = entry.get('title', 'NO TITLE')
        print(f"{index:^3}{STYLE_DIM}|{COLOR_RESET} {date_str:<10} {STYLE_DIM}|{COLOR_RESET} {STYLE_BOLD}{title[:45]:<45}{COLOR_RESET}")

    return sorted_entries

def view_entry(choice_index, entries_list):
    """
    Displays full details of the entry at choice_index.
    Removed deletion prompt.
    """
    if 0 <= choice_index < len(entries_list):
        selected_entry = entries_list[choice_index]

        print()
        print(f"{COLOR_CYAN}Title:{COLOR_RESET}       {STYLE_BOLD}{selected_entry.get('title')}{COLOR_RESET}")
        print(f"{COLOR_CYAN}Timestamp:{COLOR_RESET}   {format_timestamp(selected_entry.get('timestamp'))}")
        print(f"{COLOR_CYAN}Folder:{COLOR_RESET}      {selected_entry.get('data_folder')}")
        print(f"{COLOR_CYAN}File:{COLOR_RESET}        {ENTRY_FILENAME}")
        print("\nDescription:")
        print(selected_entry.get('description', 'N/A')) 

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
    print(f"{COLOR_YELLOW}Enter Description (Multi-line input, press Enter on an empty line to finish):{COLOR_RESET}")
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


def filter_entries(entries, field, value):
    active = list()
    for e in entries:
        ans = e.get(field, "")
        if value in ans:
            active.append(e)
    return active

def reset_active(entries):
    return entries