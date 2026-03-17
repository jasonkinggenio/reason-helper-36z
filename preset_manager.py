import os
import json
import shutil
from pathlib import Path

# Constants for the project
PRESET_DIR = Path("path/to/your/presets")  # Update this to your presets directory
OUTPUT_DIR = Path("path/to/organized/presets")  # Update this to your output directory

def load_metadata(file_path):
    """Load metadata from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading metadata from {file_path}: {e}")
        return None

def categorize_preset(file_path):
    """Categorize a preset based on its metadata."""
    metadata = load_metadata(file_path)
    if not metadata:
        return None, None

    # Example categorization based on metadata
    category = metadata.get("category", "Uncategorized")
    name = metadata.get("name", "Unnamed")

    return category, name

def rename_and_move_preset(file_path, category, name):
    """Rename and move the preset to the appropriate category folder."""
    category_dir = OUTPUT_DIR / category
    category_dir.mkdir(exist_ok=True)  # Create category directory if it doesn't exist

    new_file_name = f"{name}.json"
    new_file_path = category_dir / new_file_name

    try:
        shutil.copy(file_path, new_file_path)
        print(f"Copied {file_path} to {new_file_path}")
    except Exception as e:
        print(f"Error moving preset {file_path} to {new_file_path}: {e}")

def organize_presets():
    """Main function to organize presets by category and rename them."""
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    for preset_file in PRESET_DIR.glob("*.json"):  # Assuming presets are in JSON format
        category, name = categorize_preset(preset_file)
        if category and name:
            rename_and_move_preset(preset_file, category, name)

if __name__ == "__main__":
    organize_presets()

# TODO: 
# - Add support for more metadata fields
# - Handle different preset file formats
# - Implement a logging system instead of print statements
# - Provide a command-line interface for user input
# - Add unit tests for better reliability
