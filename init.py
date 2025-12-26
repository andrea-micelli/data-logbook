from constants import COLOR_RED, COLOR_RESET
from pathlib import Path
import yaml
import sys

CONFIG_PATH = Path("config.yaml")
EXAMPLE_PATH = Path("config.example.yaml")
DEFAULT_ENTRY_FILENAME = "description.md"

def load_config():
    if not CONFIG_PATH.exists():
        print("No config.yaml found.")

        # Copy example if it exists
        if EXAMPLE_PATH.exists():
            CONFIG_PATH.write_text(EXAMPLE_PATH.read_text())
        else:
            CONFIG_PATH.write_text(f"data_dir: /path/to/your/data/folder\ndata_filename: {DEFAULT_ENTRY_FILENAME}")

        print("A config.yaml file has been created.")
        print("Please edit it and set 'data_dir' to a valid path.")
        input("\nPress any button to close...")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    data_dir = Path(config["data_dir"])
    if not data_dir.exists():
        print(f"Configured data directory does not exist: {data_dir}")
        print("Please edit the 'data_dir' field in the 'config.yaml' file.")
        input("\nPress any button to close...")
        raise ValueError(f"Configured data_dir does not exist: {data_dir}")

    try:
        data_filename = config["data_filename"]
    except KeyError:
        print(f"{COLOR_RED}[Error] Could not retreive data_filename from config.yaml. Check that Config.yaml is correctly formatted.{COLOR_RESET}")
        input("\nPress any button to close...")
        sys.exit(1)

    return data_dir, data_filename

DEFAULT_DATA_FOLDER_ROOT, ENTRY_FILENAME = load_config()
