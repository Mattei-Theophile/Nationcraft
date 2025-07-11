import re

from nationsglory.config.settings import PathGestion

def parse_nationsgui_hdv_mappings(log_file=None):
    """
    Parse [NationsGUI] HDV Mappings entries from ForgeModLoader-client-0.log

    Args:
        log_file: Path to the ForgeModLoader-client-0.log file (autodetected if None)

    Returns:
        Set of tuples (item_id, metadata, name)
    """
    # Find ForgeModLoader-client-0.log if not provided
    if log_file is None:
        # Find Minecraft directory
        path = PathGestion()
        log_file = path.get_mod_loaders()

        # If the main log file doesn't exist, check in the logs directory
        if not log_file:

            print(f"Log file not found: {log_file}")
            return set()

    # Parse the log file for HDV Mappings entries
    hdv_mappings = set()

    try:

            for line in log_file:
                # Look for [NationsGUI] HDV Mappings entries
                match = re.search(
                    r'\[NationsGUI\] HDV Mappings: Item: (\d+):(\d+) - Category: ([a-f0-9-]+) - Name: (.+)', line)
                if match:
                    item_id = int(match.group(1))
                    metadata = int(match.group(2))
                    # category = match.group(3)  # Not needed for the set
                    name = match.group(4).strip()

                    # Add to set
                    hdv_mappings.add((item_id, metadata, name))

    except Exception as e:
        print(f"Error parsing log file: {e}")

    return hdv_mappings


def display_hdv_mappings(mappings):
    """
    Display the HDV mappings in a formatted way.

    Args:
        mappings: Set of tuples (item_id, metadata, name)
    """
    if not mappings:
        print("No HDV mappings found.")
        return

    print(f"Found {len(mappings)} HDV mappings:")
    print("-" * 50)
    print(f"{'Item ID':<8} {'Meta':<5} {'Name'}")
    print("-" * 50)

    # Sort by item ID then metadata for easier reading
    for item_id, metadata, name in sorted(mappings):
        print(f"{item_id:<8} {metadata:<5} {name}")


def save_hdv_mappings_to_file(mappings, output_file="../config/ids.json"):
    """
    Save HDV mappings to a JSON file.

    Args:
        mappings: Set of tuples (item_id, metadata, name)
        output_file: Path to the output file
    """
    import json

    # Convert set to a list of dictionaries for JSON serialization
    mappings_list = [
        {
            "item_id": item_id,
            "metadata": metadata,
            "name": name
        }
        for item_id, metadata, name in mappings
    ]

    # Sort by item ID then metadata
    mappings_list.sort(key=lambda x: (x["item_id"], x["metadata"]))

    # Save to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mappings_list, f, indent=2)
        print(f"HDV mappings saved to {output_file}")
    except Exception as e:
        print(f"Error saving mappings to file: {e}")

