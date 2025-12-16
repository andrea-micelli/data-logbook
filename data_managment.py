from constants import ( COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_RESET, FRONT_MATTER_DELIMITER)  # noqa: F401
import yaml
import os
from datetime import datetime
from init import DEFAULT_DATA_FOLDER_ROOT, ENTRY_FILENAME

# --- DATA MANAGEMENT FUNCTIONS (Unchanged) ---

def parse_markdown_entry(content):
    # TODO make error detection more robust
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
        return {"title": "Error: YAML Parse Fail"}, content


def load_entries():
    """Recursively scans the DEFAULT_DATA_FOLDER_ROOT for entry directories (containing ENTRY_FILENAME)
    and loads their metadata.
    """
    entries = []

    if not os.path.exists(DEFAULT_DATA_FOLDER_ROOT):
        print(f"{COLOR_YELLOW}Data directory '{DEFAULT_DATA_FOLDER_ROOT}' not found. No entries loaded.{COLOR_RESET}")
        return []

    # os.walk yields (dirpath, dirnames, filenames)
    for dirpath, dirnames, filenames in os.walk(DEFAULT_DATA_FOLDER_ROOT):
        # A 'measurement folder' is identified by the presence of ENTRY_FILENAME
        if ENTRY_FILENAME in filenames:
            entry_folder_path = dirpath
            entry_file_path = os.path.join(entry_folder_path, ENTRY_FILENAME)

            # Found an entry, no need to look in its subfolders (the current dirnames list)
            # This is done by clearing dirnames:
            dirnames[:] = []

            try:
                with open(entry_file_path, "r") as f:
                    content = f.read()

                metadata, description = parse_markdown_entry(content)

                if "title" in metadata and "timestamp" in metadata:
                    entry = metadata
                    entry["description"] = description
                    entry["data_folder"] = entry_folder_path
                    entries.append(entry)
                else:
                    print(
                        f"{COLOR_RED}Warning: Skipping {entry_file_path} (missing title/timestamp in metadata).{COLOR_RESET}"
                    )

            except Exception as e:
                print(
                    f"{COLOR_RED}Unexpected error loading entry {entry_folder_path}: {e}{COLOR_RESET}"
                )

        # If ENTRY_FILENAME is NOT in filenames, os.walk will continue into subdirectories
        # defined in dirnames

    entries.sort(key=lambda x: x.get("timestamp", datetime.min) if type(x.get("timestamp", datetime.min)) is datetime else datetime.min, reverse=True)
    return entries


def save_entry_metadata(entry, description_body):
    """Saves the entry's metadata and description body into its entry_filename file."""
    if "data_folder" not in entry:
        print(
            f"{COLOR_RED}[Error] Cannot save entry: missing 'data_folder' path.{COLOR_RESET}"
        )
        return

    entry_file_path = os.path.join(entry["data_folder"], ENTRY_FILENAME)

    try:
        os.makedirs(entry["data_folder"], exist_ok=True)

        save_metadata = {
            k: v for k, v in entry.items() if k not in ["description", "data_folder"]
        }

        yaml_front_matter = f"{FRONT_MATTER_DELIMITER}\n"
        yaml_front_matter += yaml.dump(save_metadata, default_flow_style=False)
        yaml_front_matter += f"{FRONT_MATTER_DELIMITER}\n\n"

        full_content = yaml_front_matter + description_body.strip() + "\n"

        with open(entry_file_path, "w") as f:
            f.write(full_content)

        print(f"{COLOR_GREEN}Entry saved to: {entry_file_path}{COLOR_RESET}")
    except IOError as e:
        print(
            f"{COLOR_RED}Error writing entry file {entry_file_path}: {e}{COLOR_RESET}"
        )
    except Exception as e:
        print(
            f"{COLOR_RED}An unexpected error occurred during saving: {e}{COLOR_RESET}"
        )
