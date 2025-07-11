"""
Utilities for working with Minecraft chunk data and schematics.
"""
# Standard library imports
import glob
from typing import List

# Third-party imports
import anvil
from nbtschematic import SchematicFile

# Local imports
from nationsglory.config.settings import PathGestion

# Constants
DIMENSION_PATHS = {
    "lune": "DIM-28/region",
    "mars": "DIM-29",
    "edora": "DIM-31",
    "edora asteroide": "DIM-32",
    "overworld": "region"  # Default dimension
}

# Initialize path manager
path_manager = PathGestion()


def get_mca_files(server: str, dimension: str = "overworld") -> List[str]:
    """
    Retrieve a list of .mca file paths corresponding to a specified server and
    dimension. Useful for accessing region files for a Minecraft server's world.

    :param server: The name of the server to retrieve files from.
    :type server: str
    :param dimension: The dimension for which to retrieve .mca files. Options
       include "overworld", "nether", or "end". Defaults to "overworld".
    :type dimension: str, optional
    :return: A list of file paths to .mca files for the specified server and
       dimension. If the dimension is not found, it defaults to the overworld.
    :rtype: List[str]

    """
    server_name = server.lower()
    dimension_name = dimension.lower()

    dim_path = DIMENSION_PATHS.get(dimension_name, DIMENSION_PATHS["overworld"])

    glob_pattern = f"{path_manager.ng_dir}/versions/stable/saves/mapwriter_mp_worlds/{server_name}*/{dim_path}/*.mca"
    return glob.glob(glob_pattern)


def extract_chunks_from_region_file(region_file_path: str) -> List[anvil.Chunk]:
    """
    Extracts all valid chunks from a given Minecraft region file.

    This function processes a `.mca` region file, identifying and retrieving
    all valid chunks within it. A chunk is considered valid if its location
    is not `(0, 0)` and it has defined `x` and `z` coordinates.

    :param region_file_path: The file path to the `.mca` region file to be
        processed.
    :type region_file_path: str
    :return: A list of valid chunks extracted from the region file.
    :rtype: List[anvil.Chunk]
    """
    region = anvil.Region.from_file(region_file_path)
    chunks = []

    for x in range(32):
        for z in range(32):
            if region.chunk_location(x, z) != (0, 0):
                chunk = region.get_chunk(x, z)
                if chunk.x is not None and chunk.z is not None:
                    chunks.append(chunk)

    return chunks


def extract_blocks_from_chunk(chunk: anvil.Chunk) -> List[anvil.block]:
    """
    Extracts all blocks from a given chunk.

    This function takes an `anvil.Chunk` object, streams through its data,
    and collects all the blocks into a list. It provides a convenient way
    to access all blocks contained in a chunk for further processing or
    analysis.

    :param chunk: The chunk object from which blocks are to be extracted.
    :type chunk: anvil.Chunk
    :return: A list containing all the blocks extracted from the chunk.
    :rtype: List[anvil.block]
    """
    return list(chunk.stream_chunk())


def save_chunks_as_schematic(chunk_block_lists: List[List[anvil.block]]) -> SchematicFile:
    """
    Saves a list of chunk blocks as a schematic file. Each chunk consists of a list
    of blocks, and their data is processed to create a schematic representation.
    The schematic is saved to the specified output path using the provided blocks'
    coordinates, data, and metadata. The function assumes a 3D grid-like structure
    and arranges blocks within the schematic accordingly.

    :param chunk_block_lists: A list of chunks where each chunk is a list of
        `anvil.block` objects representing the structure of blocks and containing
        data such as their coordinates and metadata.

    :return: None
    """


    
    # Shape: (y, z, x)
    schematic = SchematicFile(shape=(256, 16 * len(chunk_block_lists), 16 * len(chunk_block_lists)))

    for chunk_blocks in chunk_block_lists:
        for block in chunk_blocks:
            schematic.blocks[block.y, block.z, block.x] = block.y
            schematic.data[block.y, block.z, block.x] = block.data

    return schematic