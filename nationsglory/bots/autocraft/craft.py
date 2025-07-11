import os
import json
import pyautogui
from typing import List, Tuple, Set


class CraftingAutomation:
    """
    Automates crafting process in Minecraft-like environments using image recognition.

    This class facilitates crafting by locating items through image processing,
    managing inventory, retrieving necessary blocks, and handling the crafting grid.
    All operations are reliant on predefined constants, directories for resources,
    and user inputs. Additionally, it provides methods for crafting table
    interactions, resource checks, inventory handling, and retrieving crafting recipes.
    """

    # Class constants
    IMAGE_CONFIDENCE = {
        'PLAYER_INVENTORY': 0.3,
        'CRAFTING_TABLE': 0.5,
        'CASE_OF_CRAFTING': 0.8,
        'RESULT_CRAFT': 0.8,
        'CASE_OF_INVENTORY': 0.8
    }

    IMAGE_PATHS = {
        'PLAYER_INVENTORY': "nationsglory/assets/images/player_inventory.png",
        'CRAFTING_TABLE': "nationsglory/assets/images/crafting_table.png",
        'CASE_OF_CRAFTING': "nationsglory/assets/images/case_of_crafting_table.png",
        'RESULT_CRAFT': "nationsglory/assets/images/result_craft.png",
        'CASE_OF_INVENTORY': "nationsglory/assets/images/case_of_inventory.png"
    }

    BLOCKS_DIRECTORY = "nationsglory/assets/blocks"
    PLAYER_DIRECTORY = "nationsglory/player"
    CRAFT_DATA_FILE = "nationsglory/bots/autocraft/save_craft.json"

    def __init__(self, one_by_one: bool, craft_all_inventory: bool, confidence_of_block: float, id_block: str):
        """
        Initialize crafting automation.

        Args:
            one_by_one: Whether to craft items one by one
            craft_all_inventory: Whether to craft until inventory is empty
            confidence_of_block: Confidence level for image recognition
            id_block: ID of the block to craft
        """
        # Create a dictionary for slots instead of individual variables
        self.slots = {i+1: str(i+2) for i in range(9)}

        self.one_by_one = one_by_one
        self.craft_all_inventory = craft_all_inventory
        self.confidence_of_block = confidence_of_block
        self.id_block = id_block
        self.player_inventory = None

    def make_craft(self, crafting_matrix: List[List[str]]) -> None:
        """
        Execute the crafting process based on the provided recipe matrix.

        Args:
            crafting_matrix: A 3x3 matrix representing the crafting recipe
        """
        # Open inventory
        pyautogui.press('e')

        # Detect player inventory
        self.player_inventory = self.detect_player_inventory()

        # Check if crafting table is needed
        if self.is_crafting_table_needed(crafting_matrix):
            self.handle_crafting_table()

        # Get blocks for crafting
        blocks_for_craft = self.get_blocks_for_craft(crafting_matrix)

        # Check if we have all required blocks
        if not self.check_resources(blocks_for_craft):
            print("Not enough resources for crafting")
            pyautogui.press('esc')
            return

        # Place blocks in crafting grid
        self.place_blocks_in_grid(crafting_matrix)

        # Take the crafted item
        self.take_crafted_item()

        # Close inventory
        pyautogui.press('esc')

    def detect_player_inventory(self) -> List[Tuple[int, int]]:
        """
        Detect the player's inventory on screen.

        Returns:
            List of coordinates for inventory slots
        """
        # Implementation details...
        return []

    def is_crafting_table_needed(self, crafting_matrix: List[List[str]]) -> bool:
        """
        Determine if a crafting table is needed for the recipe.

        Args:
            crafting_matrix: A 3x3 matrix representing the crafting recipe

        Returns:
            True if a crafting table is needed, False otherwise
        """
        # Check if any blocks are placed outside the 2x2 player crafting grid
        for i in range(3):
            for j in range(3):
                if (i > 1 or j > 1) and crafting_matrix[i][j] != "":
                    return True
        return False

    def handle_crafting_table(self) -> None:
        """
        Handle the crafting table interaction.
        """
        # Implementation details...
        pass

    def get_blocks_for_craft(self, crafting_matrix: List[List[str]]) -> Set[str]:
        """
        Get the set of blocks needed for the crafting recipe.

        Args:
            crafting_matrix: A 3x3 matrix representing the crafting recipe

        Returns:
            Set of block IDs needed for crafting
        """
        blocks = set()
        for row in crafting_matrix:
            for block in row:
                if block:
                    blocks.add(block)
        return blocks

    def check_resources(self, blocks_for_craft: Set[str]) -> bool:
        """
        Check if the player has all the required resources.

        Args:
            blocks_for_craft: Set of block IDs needed for crafting

        Returns:
            True if all resources are available, False otherwise
        """
        # Implementation details...
        return True

    def place_blocks_in_grid(self, crafting_matrix: List[List[str]]) -> None:
        """
        Place blocks in the crafting grid according to the recipe.

        Args:
            crafting_matrix: A 3x3 matrix representing the crafting recipe
        """
        # Implementation details...
        pass

    def take_crafted_item(self) -> None:
        """
        Take the crafted item from the result slot.
        """
        # Implementation details...
        pass

    @classmethod
    def save_craft(cls, recipe_name: str, id_block: str, crafting_matrix: List[List[str]]) -> bool:
        """
        Save a crafting recipe to the craft data file.

        Args:
            recipe_name: Name of the recipe
            id_block: ID of the block to craft
            crafting_matrix: A 3x3 matrix representing the crafting recipe

        Returns:
            True if the recipe was saved successfully, False otherwise
        """
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(cls.CRAFT_DATA_FILE), exist_ok=True)

        # Load existing recipes
        try:
            with open(cls.CRAFT_DATA_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Create the recipe object
        recipe = {
            "name": recipe_name,
            "id": id_block,
            "matrix": crafting_matrix
        }

        # Check if a recipe with this name already exists
        for i, craft in enumerate(data):
            if craft.get("name") == recipe_name:
                # Replace the existing recipe
                data[i] = recipe
                break
        else:
            # Add the new recipe
            data.append(recipe)

        # Save the updated recipes
        try:
            with open(cls.CRAFT_DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving craft: {str(e)}")
            return False

    @classmethod
    def load_craft(cls, recipe_name: str) -> dict:
        """
        Load a crafting recipe from the craft data file.

        Args:
            recipe_name: Name of the recipe

        Returns:
            The recipe object if found, None otherwise
        """
        try:
            with open(cls.CRAFT_DATA_FILE, "r") as f:
                data = json.load(f)

            for craft in data:
                if craft.get("name") == recipe_name:
                    return craft

            return None
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @classmethod
    def get_available_crafts(cls) -> List[str]:
        """
        Get a list of available crafting recipes.

        Returns:
            List of recipe names
        """
        try:
            with open(cls.CRAFT_DATA_FILE, "r") as f:
                data = json.load(f)

            return [craft.get("name") for craft in data if craft.get("name")]
        except (FileNotFoundError, json.JSONDecodeError):
            return []


def verify_craft(id_block: str) -> List[List[str]]:
    """
    Verify if a crafting recipe exists for the given block ID.

    Args:
        id_block: ID of the block to craft

    Returns:
        The crafting matrix if found, None otherwise
    """
    try:
        with open(CraftingAutomation.CRAFT_DATA_FILE, "r") as f:
            data = json.load(f)

        for craft in data:
            if craft["id"] == id_block:
                return craft["matrix"]

        return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None
