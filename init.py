from pathlib import Path
import yaml
import sys

CONFIG_PATH = Path("config.yaml")
EXAMPLE_PATH = Path("config.example.yaml")

def load_config():
    if not CONFIG_PATH.exists():
        print("No config.yaml found.")

        # Copy example if it exists
        if EXAMPLE_PATH.exists():
            CONFIG_PATH.write_text(EXAMPLE_PATH.read_text())
        else:
            CONFIG_PATH.write_text("data_dir: /path/to/your/data/folder\n")

        print("A config.yaml file has been created.")
        print("Please edit it and set 'data_dir' to a valid path.")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    data_dir = Path(config["data_dir"])
    if not data_dir.exists():
        raise ValueError(f"Configured data_dir does not exist: {data_dir}")

    return data_dir

DEFAULT_DATA_FOLDER_ROOT = load_config()
