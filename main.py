from constants import (COLOR_BLUE,COLOR_GREEN,COLOR_YELLOW,COLOR_RED,COLOR_RESET,ENTRY_FILENAME,DEFAULT_DATA_FOLDER_ROOT,FRONT_MATTER_DELIMITER,STYLE_BOLD,)  # noqa: F401
from commands import (list_entries,view_entry,open_entry_folder,open_in_editor,edit_markdown,edit_entry,create_entry,)  # noqa: F401
from data_managment import (parse_markdown_entry,load_entries,save_entry_metadata,)  # noqa: F401


def main():
    entries = load_entries()

    print(f"{STYLE_BOLD}{COLOR_BLUE}Measurement Logbook{COLOR_RESET}\n")

    sorted_entries = list_entries(entries)  # Initial list display

    print(f"\n{COLOR_YELLOW}Enter 'help' for commands, or 'quit' to exit.{COLOR_RESET}")

    while True:
        try:
            cmd_line = input(f"{COLOR_BLUE}logbook> {COLOR_RESET}").strip()
            if not cmd_line:
                print("{COLOR_YELLOW}[warning]: skipped input, reloading input{COLOR_RESET}")
                continue

            parts = cmd_line.split()  # Splits on spaces, separates keywords
            command = parts[0].lower()  # First keyword is the command
            args = parts[1:]  # the others are the arguments

            # COMMANDS MATCH STATEMENT
            match command:

                case "quit" | "exit" | "qt":  # Terminates the program
                    print("\nExiting Logbook Manager. Goodbye!")
                    break

                case "list" | "ls":  # Lists all measurements
                    sorted_entries = list_entries(entries)

                case "new" | "nw":  # Creates new entry
                    create_entry(entries)
                    sorted_entries = list_entries(entries)

                case "open" | "op":  # Opens the folder containing the measurements
                    if not args:  # if arg list is empty
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

                case "show" | "sw":  # Open full description
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

                case "edit" | "ed":  # Open log_entry.md in editor
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

                case "help" | "hp":
                    print(f"\n{COLOR_BLUE}--- Available Commands ---{COLOR_RESET}")
                    print(f"{COLOR_GREEN}new{COLOR_RESET}               : Create a new logbook entry (creates folder and {ENTRY_FILENAME}).")
                    print(f"{COLOR_GREEN}list (or ls){COLOR_RESET}      : Display the chronological list of entries.")
                    print(f"{COLOR_GREEN}show <number>{COLOR_RESET}     : Select an entry to view metadata and raw Markdown.")
                    print(f"{COLOR_GREEN}open <number>{COLOR_RESET}     : Open the entry's folder in file explorer and select the {ENTRY_FILENAME} file.")
                    print(f"{COLOR_GREEN}edit <number>{COLOR_RESET}     : Open the log_entry.md file in the default editor.")
                    print(f"{COLOR_GREEN}quit (or exit){COLOR_RESET}    : Exit the application.")
                    print(f"{COLOR_BLUE}--------------------------{COLOR_RESET}")

                case _:
                    print(f"{COLOR_RED}[Error] Unknown command: '{command}'. Try 'help'.{COLOR_RESET}")

        except EOFError:
            print("\nExiting Logbook Manager. Goodbye!")
            break
        except Exception as e:
            print(f"{COLOR_RED}[Fatal Error] An unhandled error occurred: {e}{COLOR_RESET}")
            break


if __name__ == "__main__":
    main()
