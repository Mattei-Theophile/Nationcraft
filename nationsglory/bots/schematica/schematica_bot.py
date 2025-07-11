import nbtschematic as nbschem
import numpy as np
import os
import json
from nationsglory.bots.player.bots import Player
from nationsglory.config import settings
from typing import List, Dict, Tuple, Optional, Union
import time

class SchematicaBot:
    """
    A class for handling Minecraft schematics, including loading, analyzing, and building them.
    """
    def __init__(self, player=None):
        """
        Initialize the SchematicaBot with a player instance.

        Args:
            player: An instance of the Player class for executing movements
        """
        self.player = player if player else Player()
        self.current_schematic = None
        self.schematic_name = None
        self.schematic_dir = os.path.join(settings.PathGestion().get_ng_dir(), "assets", "schematics")

        # Create the schematics directory if it doesn't exist
        if not os.path.exists(self.schematic_dir):
            os.makedirs(self.schematic_dir)

    def load_schematic_file(self, file_path: str) -> nbschem.SchematicFile:
        """
        Load a schematic file from the given path.

        Args:
            file_path: Path to the schematic file

        Returns:
            The loaded SchematicFile object
        """
        try:
            self.current_schematic = nbschem.SchematicFile.load(file_path)
            self.schematic_name = os.path.basename(file_path).split('.')[0]
            return self.current_schematic
        except Exception as e:
            print(f"Error loading schematic file: {str(e)}")
            return None

    def get_schematic_info(self) -> Dict:
        """
        Get information about the currently loaded schematic.

        Returns:
            A dictionary containing information about the schematic
        """
        if not self.current_schematic:
            return {"error": "No schematic loaded"}

        shape = self.current_schematic.shape
        blocks = np.array(self.current_schematic.blocks)
        data = np.array(self.current_schematic.data)

        # Count the occurrences of each block type
        block_counts = {}
        for y in range(shape[0]):
            for z in range(shape[1]):
                for x in range(shape[2]):
                    block_id = int(blocks[y, z, x])
                    if block_id in block_counts:
                        block_counts[block_id] += 1
                    else:
                        block_counts[block_id] = 1

        return {
            "name": self.schematic_name,
            "dimensions": {
                "height": shape[0],
                "width": shape[1],
                "length": shape[2]
            },
            "block_counts": block_counts,
            "total_blocks": np.sum(blocks > 0)  # Count non-air blocks
        }

    def get_block_at(self, x: int, y: int, z: int) -> Tuple[int, int]:
        """
        Get the block ID and data value at the specified coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate

        Returns:
            A tuple containing the block ID and data value
        """
        if not self.current_schematic:
            return (0, 0)  # Air block

        shape = self.current_schematic.shape
        if 0 <= y < shape[0] and 0 <= z < shape[1] and 0 <= x < shape[2]:
            block_id = int(self.current_schematic.blocks[y, z, x])
            data_val = int(self.current_schematic.data[y, z, x])
            return (block_id, data_val)
        else:
            return (0, 0)  # Air block

    def get_layer(self, y: int) -> np.ndarray:
        """
        Get a 2D array representing a horizontal layer of the schematic.

        Args:
            y: The Y coordinate of the layer

        Returns:
            A 2D numpy array containing block IDs for the layer
        """
        if not self.current_schematic:
            return np.array([])

        shape = self.current_schematic.shape
        if 0 <= y < shape[0]:
            return np.array(self.current_schematic.blocks[y])
        else:
            return np.array([])

    def build_layer(self, y: int, start_x: int = 0, start_z: int = 0) -> bool:
        """
        Build a single layer of the schematic.

        Args:
            y: The Y coordinate of the layer to build
            start_x: The X coordinate to start building from
            start_z: The Z coordinate to start building from

        Returns:
            True if the layer was built successfully, False otherwise
        """
        if not self.current_schematic or not self.player:
            return False

        layer = self.get_layer(y)
        if layer.size == 0:
            return False

        shape = self.current_schematic.shape

        # Move to the starting position
        # This is a simplified approach; in a real implementation, you would need
        # to handle positioning the player correctly

        # Build the layer by placing blocks
        for z in range(shape[1]):
            for x in range(shape[2]):
                block_id, data_val = self.get_block_at(x, y, z)
                if block_id > 0:  # Skip air blocks
                    # Select the appropriate block in the hotbar
                    # This is a simplified approach; in a real implementation, you would need
                    # to handle inventory management and block selection

                    # Place the block
                    self.player.use()

                # Move to the next position
                if x < shape[2] - 1:
                    self.player.move("right", 1)

            # Move to the start of the next row
            if z < shape[1] - 1:
                self.player.move("backward", shape[2] - 1)
                self.player.move("right", 1)

        return True

    def build_schematic(self, start_y: int = 0, end_y: Optional[int] = None) -> bool:
        """
        Build the entire schematic or a range of layers.

        Args:
            start_y: The Y coordinate to start building from
            end_y: The Y coordinate to end building at (inclusive)

        Returns:
            True if the schematic was built successfully, False otherwise
        """
        if not self.current_schematic:
            return False

        shape = self.current_schematic.shape
        if end_y is None:
            end_y = shape[0] - 1

        # Validate the range
        if start_y < 0 or start_y >= shape[0] or end_y < start_y or end_y >= shape[0]:
            return False

        # Build each layer
        for y in range(start_y, end_y + 1):
            success = self.build_layer(y)
            if not success:
                return False

            # Move up to the next layer if not the last layer
            if y < end_y:
                # This is a simplified approach; in a real implementation, you would need
                # to handle moving up to the next layer
                pass

        return True

    def save_schematic(self, file_name: str) -> bool:
        """
        Save the current schematic to a file.

        Args:
            file_name: The name of the file to save the schematic to

        Returns:
            True if the schematic was saved successfully, False otherwise
        """
        if not self.current_schematic:
            return False

        file_path = os.path.join(self.schematic_dir, f"{file_name}.schematic")
        try:
            self.current_schematic.save(file_path)
            return True
        except Exception as e:
            print(f"Error saving schematic: {str(e)}")
            return False

    def get_available_schematics(self) -> List[str]:
        """
        Get a list of available schematic files.

        Returns:
            A list of schematic file names without the extension
        """
        try:
            return [f[:-10] for f in os.listdir(self.schematic_dir) if f.endswith('.schematic')]
        except Exception as e:
            print(f"Error getting schematics: {str(e)}")
            return []

# Create a singleton instance
schematica_bot = SchematicaBot()

# Legacy functions for backward compatibility
def load_schematic_file(file):
    return schematica_bot.load_schematic_file(file)

def get_block_by_layer(file, layer, shape):
    if not schematica_bot.current_schematic:
        schematica_bot.load_schematic_file(file)
    return schematica_bot.get_layer(layer)
