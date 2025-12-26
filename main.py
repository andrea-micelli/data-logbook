from constants import (COLOR_BLUE,COLOR_GREEN,COLOR_YELLOW,COLOR_RED,COLOR_BRIGHT_BLUE,COLOR_RESET,FRONT_MATTER_DELIMITER,STYLE_BOLD,STYLE_DIM,STYLE_ITALIC)  # noqa: F401
from commands import (list_entries,view_entry,open_entry_folder,open_in_editor,edit_markdown,edit_entry,create_entry,filter_entries,reset_active)  # noqa: F401
from data_managment import (parse_markdown_entry,load_entries,save_entry_metadata,)  # noqa: F401
from utility import print_help, print_help_command
import traceback
import sys
from version import __version__

def main():

    entries = load_entries()
    active = entries

    print(f"{STYLE_BOLD}{COLOR_BRIGHT_BLUE}{' MEASUREMENTS LOGBOOK ':=^80}{COLOR_RESET}")
    print(f"Github repository: {STYLE_ITALIC}https://github.com/andrea-micelli/data-logbook.git{COLOR_RESET}")
    print(f"Current verion: {STYLE_ITALIC}v{__version__}{COLOR_RESET}\n")

    active_filter = dict()
    list_entries(active, active_filter)  # Initial list display

    print(f"\n{COLOR_YELLOW}Enter 'help' for commands, or 'quit' to exit.{COLOR_RESET}")

    while True:
        try:
            cmd_line = input(f"{STYLE_BOLD}> {COLOR_RESET}").strip()
            if not cmd_line:
                print(f"{COLOR_YELLOW}[warning]: skipped input, reloading input{COLOR_RESET}")
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
                    list_entries(active, active_filter)

                case "new" | "nw":  # Creates new entry
                    create_entry(entries)
                    active = reset_active(entries)
                    list_entries(active, active_filter)

                case "open" | "op":  # Opens the folder containing the measurements
                    if not args:  # if arg list is empty
                        print(f"{COLOR_RED}[Error] Usage: open <entry_number>{COLOR_RESET}")
                        continue

                    try:
                        entry_number = int(args[0])
                        if active:
                            index = entry_number - 1
                            open_entry_folder(index, active)
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
                        if active:
                            index = entry_number - 1
                            view_entry(index, active)
                        else:
                            print(f"{COLOR_RED}[Error] No entries to show.{COLOR_RESET}")
                    except ValueError:
                        print(f"{COLOR_RED}[Error] Invalid entry number provided. Must be an integer.{COLOR_RESET}")

                case "edit" | "ed":  # Open log_entry.md in editor
                    if not args:
                        print(f"{COLOR_RED}[Error] Usage: edit <entry_number>{COLOR_RESET}")
                        continue
                    try:
                        entry_number = int(args[0])
                        if active:
                            index = entry_number - 1
                            edit_success = edit_markdown(index, active)
                            if edit_success:
                                entries.clear()
                                entries.extend(load_entries())
                                active = reset_active(entries) # TODO implementare qui un recupero dei filtri invece di un reset
                                list_entries(active, active_filter)
                        else:
                            print(f"{COLOR_RED}[Error] No entries to edit. Use 'new' to create one.{COLOR_RESET}")
                    except ValueError:
                        print(f"{COLOR_RED}[Error] Invalid entry number provided. Must be an integer.{COLOR_RESET}")

                case "search" | "src":
                    if len(args) != 2:
                        print("[Error] Correct usage: 'search <field> <text>'")
                        continue
                    active_filter[args[0]] = args[1]
                    active = filter_entries(active, field=args[0], value=args[1])
                    list_entries(active, active_filter)

                    
                case "reset" | "rst":
                    active = reset_active(entries)
                    active_filter = dict()
                    list_entries(active, active_filter)

                case "help" | "hp":
                    if len(args) == 0:
                        print_help()
                    elif len(args) == 1:
                        print_help_command(args[0])
                    else:
                        print("[Error] Incorrect usage. Correct usage is 'help' for the command list, or 'help <command>' for help for a specific command.")

                case _:
                    print(f"{COLOR_RED}[Error] Unknown command: '{command}'. Try 'help'.{COLOR_RESET}")

        except EOFError:
            print("\nExiting Logbook Manager. Goodbye!")
            break
        except Exception as e:
            print(f"{COLOR_RED}[Fatal Error] An unhandled error occurred: {e}{COLOR_RESET}")
            break


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\n\n An unexpected error occurred:\n")
        traceback.print_exc()

        print("\nPress Enter to exit...")
        input()

        sys.exit(1)
