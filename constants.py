# --- ANSI COLOR CODES (Foreground) ---
COLOR_BLACK   = '\033[30m'
COLOR_RED     = '\033[31m'
COLOR_GREEN   = '\033[32m'
COLOR_YELLOW  = '\033[33m'
COLOR_BLUE    = '\033[34m'
COLOR_MAGENTA = '\033[35m'
COLOR_CYAN    = '\033[36m'
COLOR_WHITE   = '\033[37m'

# Bright variants
COLOR_BRIGHT_BLACK   = '\033[90m'  # Often shown as gray
COLOR_BRIGHT_RED     = '\033[91m'
COLOR_BRIGHT_GREEN   = '\033[92m'
COLOR_BRIGHT_YELLOW  = '\033[93m'
COLOR_BRIGHT_BLUE    = '\033[94m'
COLOR_BRIGHT_MAGENTA = '\033[95m'
COLOR_BRIGHT_CYAN    = '\033[96m'
COLOR_BRIGHT_WHITE   = '\033[97m'

# --- ANSI TEXT STYLE CODES ---
STYLE_RESET       = '\033[0m'   # Reset all styles
STYLE_BOLD        = '\033[1m'
STYLE_DIM         = '\033[2m'
STYLE_ITALIC      = '\033[3m'
STYLE_UNDERLINE   = '\033[4m'
STYLE_BLINK       = '\033[5m'
STYLE_INVERT      = '\033[7m'   # Swap foreground/background
STYLE_HIDDEN      = '\033[8m'
STYLE_STRIKE      = '\033[9m'

# Reset
COLOR_RESET = '\033[0m'


# --- CONFIGURATION ---
ENTRY_FILENAME = 'log_entry.md'
DEFAULT_DATA_FOLDER_ROOT = 'data' 
FRONT_MATTER_DELIMITER = '---'