from constants import COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_RESET, ENTRY_FILENAME, DEFAULT_DATA_FOLDER_ROOT, FRONT_MATTER_DELIMITER, STYLE_BOLD # noqa: F401
from commands import list_entries, view_entry, open_entry_folder, open_in_editor, edit_markdown, edit_entry, create_entry # noqa: F401
from data_managment import parse_markdown_entry, load_entries, save_entry_metadata  # noqa: F401

# --- MAIN EXECUTION (CLI) ---

def main():
    """Main function to run the logbook application with a command-line interface."""

    print(f"{STYLE_BOLD}{COLOR_BLUE}Measurement Logbook{COLOR_RESET}")
    print()
    
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
                print(f"{COLOR_GREEN}show <number>{COLOR_RESET}      : Select an entry to view metadata and raw Markdown.")
                print(f"{COLOR_GREEN}open <number>{COLOR_RESET}     : Open the entry's folder in file explorer and select the {ENTRY_FILENAME} file.")
                print(f"{COLOR_GREEN}edit <number>{COLOR_RESET}     : Open the log_entry.md file in the default editor.")
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