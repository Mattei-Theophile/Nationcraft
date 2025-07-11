import os
import json
import time
import pyautogui
from typing import List, Dict, Any, Tuple


class SearchCrafting:
    """
    Class for searching and detecting crafting recipes in Minecraft.
    
    This class provides functionality to open the crafting interface,
    detect items in the crafting grid, create a matrix representation
    of the crafting recipe, and save it for later use.
    """
    
    # Class constants
    CRAFT_DATA_FILE = "nationsglory/bots/autocraft/save_craft.json"
    BLOCKS_DIRECTORY = "nationsglory/assets/blocks"
    
    def __init__(self, id_block: str):
        """
        Initialize the search crafting functionality.
        
        Args:
            id_block: ID of the block to search for
        """
        self.id_block = id_block
        self.matrix_of_craft = []
        
    def open_craft(self) -> None:
        """
        Open the crafting interface.
        """
        # Press 'e' to open inventory
        pyautogui.press('e')
        time.sleep(0.5)
        
    def detect_craft(self) -> List[Dict[str, Any]]:
        """
        Detect items in the crafting grid.
        
        Returns:
            List of dictionaries containing information about detected items
        """
        # Implementation details...
        return []
        
    def create_matrix_of_craft(self, list_of_item: List[Dict[str, Any]]) -> None:
        """
        Create a matrix representation of the crafting recipe.
        
        Args:
            list_of_item: List of dictionaries containing information about detected items
        """
        # Initialize 3x3 matrix with empty strings
        self.matrix_of_craft = [["" for _ in range(3)] for _ in range(3)]
        
        # Fill matrix with detected items
        for item in list_of_item:
            row = item.get("row", 0)
            col = item.get("col", 0)
            block_id = item.get("id", "")
            
            if 0 <= row < 3 and 0 <= col < 3:
                self.matrix_of_craft[row][col] = block_id
                
    def save_craft(self) -> None:
        """
        Save the crafting recipe to a JSON file.
        """
        # Create data structure for the craft
        craft_data = {
            "id": self.id_block,
            "matrix": self.matrix_of_craft
        }
        
        try:
            # Load existing data if file exists
            if os.path.exists(self.CRAFT_DATA_FILE):
                with open(self.CRAFT_DATA_FILE, "r") as f:
                    data = json.load(f)
            else:
                data = []
                
            # Check if craft already exists
            for i, craft in enumerate(data):
                if craft["id"] == self.id_block:
                    # Update existing craft
                    data[i] = craft_data
                    break
            else:
                # Add new craft
                data.append(craft_data)
                
            # Save data
            with open(self.CRAFT_DATA_FILE, "w") as f:
                json.dump(data, f, indent=4)
                
            print(f"Craft for {self.id_block} saved successfully")
            
        except Exception as e:
            print(f"Error saving craft: {e}")
            
    def detect_item_at_position(self, x: int, y: int) -> Tuple[bool, str]:
        """
        Detect an item at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple containing a boolean indicating if an item was detected
            and the ID of the detected item
        """
        # Implementation details...
        return False, ""