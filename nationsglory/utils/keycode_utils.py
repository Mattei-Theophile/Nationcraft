import json
import os

# Constants
OPTIONS_FILE_PATH = os.path.expanduser("~/.NationsGlory/versions/stable/options.txt")
KEYCODE_FILE_PATH = "../nationsglory-bot/keycode.json"

def get_keycode_number(name_keycode, options_content):
    """
    Extract keycode number from options file content.
    
    Args:
        name_keycode (str): The name of the keycode to find
        options_content (list): The content of the options file
        
    Returns:
        int: The keycode number
        
    Raises:
        ValueError: If the keycode is not found
    """
    for line in options_content:
        if name_keycode in line:
            return int(line.split(":")[1])
    raise ValueError(f"Keycode '{name_keycode}' not found in options file")

def get_letter_from_keycode_number(keycode_number, keycode_mapping):
    """
    Find the letter corresponding to a keycode number.
    
    Args:
        keycode_number (int): The keycode number
        keycode_mapping (dict): The keycode mapping
        
    Returns:
        str: The letter corresponding to the keycode number
        
    Raises:
        ValueError: If no letter is found for the keycode number
    """
    for key, value in keycode_mapping.items():
        if value == keycode_number:
            return key
    raise ValueError(f"No letter found for keycode number {keycode_number}")

def convert_keycode_to_letter(name_keycode, options_file_path=OPTIONS_FILE_PATH, keycode_file_path=KEYCODE_FILE_PATH):
    """
    Convert a keycode name to its corresponding letter.
    
    Args:
        name_keycode (str): The name of the keycode to convert
        options_file_path (str, optional): The path to the options file
        keycode_file_path (str, optional): The path to the keycode mapping file
        
    Returns:
        str: The letter corresponding to the keycode name, or None if an error occurs
    """
    try:
        # Read options file
        with open(options_file_path, "r") as file:
            options_content = file.readlines()

        # Get keycode number
        keycode_number = get_keycode_number(name_keycode, options_content)

        # Load keycode mapping
        with open(keycode_file_path, "r") as file:
            keycode_mapping = json.load(file)

        # Get letter from keycode number
        return get_letter_from_keycode_number(keycode_number, keycode_mapping)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error converting keycode: {e}")
        return None