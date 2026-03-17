import os
import json
import glob

def load_presets_metadata(directory):
    """
    Load preset metadata from JSON files in the given directory.
    
    Args:
        directory (str): The directory where preset JSON files are stored.
    
    Returns:
        list: A list of metadata dictionaries for each preset.
    """
    metadata_list = []
    filepath = None
    try:
        for filepath in glob.glob(os.path.join(directory, '*.json')):
            with open(filepath, 'r') as file:
                metadata = json.load(file)
                metadata_list.append(metadata)
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {filepath if filepath else 'unknown'}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return metadata_list


def rename_preset_file(original_path, new_path):
    """
    Rename a preset file to a new path.
    
    Args:
        original_path (str): The current path of the preset file.
        new_path (str): The new path for the preset file.
    
    Returns:
        bool: True if the renaming was successful, False otherwise.
    """
    try:
        os.rename(original_path, new_path)
        print(f'Renamed "{original_path}" to "{new_path}"')
        return True
    except FileNotFoundError:
        print(f"File not found: {original_path}")
    except PermissionError:
        print(f"Permission denied when trying to rename: {original_path}")
    except Exception as e:
        print(f"An unexpected error occurred during renaming: {e}")

    return False


def organize_presets_by_category(metadata_list, base_directory):
    """
    Organize presets into directories based on their categories in the metadata.

    Args:
        metadata_list (list): A list of metadata dictionaries for each preset.
        base_directory (str): The base directory where presets are stored.
    
    Returns:
        None
    """
    for metadata in metadata_list:
        category = metadata.get('category', 'Uncategorized')
        preset_name = metadata.get('name', 'UnknownPreset')
        original_path = os.path.join(base_directory, f"{preset_name}.json")

        # Check if the original file exists before attempting to rename
        if not os.path.exists(original_path):
            print(f"File not found: {original_path}")
            continue

        category_dir = os.path.join(base_directory, category)
        os.makedirs(category_dir, exist_ok=True)  # Create category directory if it doesn't exist

        # Move preset file to the new category directory
        new_name = f"{preset_name}_{category}.json"
        new_path = os.path.join(category_dir, new_name)
        rename_preset_file(original_path, new_path)


# TODO: Add support for other metadata formats (e.g., XML)
# TODO: Implement logging instead of print statements
# TODO: Enhance error handling and user notifications
# TODO: Consider a way to handle duplicates in naming

if __name__ == "__main__":
    # Example usage: Load metadata and organize presets
    presets_directory = 'path/to/presets'
    presets_metadata = load_presets_metadata(presets_directory)
    organize_presets_by_category(presets_metadata, presets_directory)
