from nationsglory.bots.xray import chunks
import anvil
from typing import Dict, List, Tuple
import json
import os



def load_block_id():
    """Load block IDs from ids.json configuration file."""
    config_path = os.path.join('nationsglory', 'config', 'ids.json')
    with open(config_path, 'r') as f:
        return json.load(f)

def find_blocks_by_id(block_id: int, block_data:int, blocks: List[anvil.block]) -> List[Dict[str, int]]:
    """
    Finds and returns the coordinates of all blocks with a specific block ID from a list of blocks.

    This function iterates through a list of block objects and checks for blocks
    with a matching ID. When a match is found, the function collects the block's
    coordinates (x, y, z) and stores them in a dictionary format. The final result
    is a list of these coordinate dictionaries.

    :param block_id: The ID of the block to search for.
    :type block_id: int
    :param blocks: A list of blocks to search, where each block has attributes `id`, `x`, `y`, and `z`.
    :type blocks: List[anvil.block]
    :return: A list of dictionaries, each containing the coordinates of blocks (`x`, `y`, `z`) that match the given ID.
    :rtype: List[Dict[str, int]]
    """
    cpt = 0
    for block in blocks:
        if block_id == block.id and block_data == block.data:
            cpt += 1
    return cpt

def find_blocks_in_chunks(block_id: int, chunk_list: List[anvil.Chunk]) -> List[Dict[Tuple[int, int], int]]:
    """
    Finds the occurrences of a specific block ID within a list of chunks and returns
    a summary of the count of those blocks per chunk.

    This function scans through a list of chunks, analyzes their block matrices,
    and determines the number of occurrences for the specified block ID.
    The result provides a mapping of chunk coordinates to the count of the block's
    presence, making it useful for summarizing block distributions.

    :param block_id: The ID of the block to search for within the provided chunks.
    :type block_id: int
    :param chunk_list: A list of chunks to analyze. Each chunk must have properties
        for accessing its block matrices and coordinate information (x, z).
    :type chunk_list: List[anvil.Chunk]
    :return: A list of dictionaries where each dictionary maps a tuple of chunk
        coordinates (x, z) to the count of matching blocks within the corresponding chunk.
    :rtype: List[Dict[Tuple[int, int], int]]
    """
    results = []
    for chunk in chunk_list:
        coordinates = find_blocks_by_id(block_id, chunks.extract_blocks_from_chunk(chunk))
        results.append({(chunk.x, chunk.z): coordinates})
    return results


def count_blocks_in_chunk(chunk_blocks: List[anvil.block]) -> Dict[str, int]:
    """
    Counts the occurrences of each block type in a chunk and returns a dictionary
    mapping block names to their counts. Non-air blocks are considered, and block
    names are retrieved from ids.json. If a block name is not available
    in the mapping, the string representation of its ID is used.

    :param chunk_blocks: A list of block objects from the chunk.
    :return: A dictionary where keys are block names and values are their
             corresponding counts.
    :rtype: Dict[str, int]
    """
    block_counts = {}
    block_data = load_block_id()

    # Create a dictionary to map (item_id, metadata) to block name
    block_mapping = {}
    for item in block_data:
        key = (item["item_id"], item["metadata"])
        block_mapping[key] = item["name"]

    for block in chunk_blocks:
        # Skip air blocks
        if block.id == 0:
            continue

        # Get block name from the mapping or use string ID as fallback
        block_key = (block.id, block.data)
        block_name = block_mapping.get(block_key)

        # Try with metadata 0 as fallback if specific metadata not found
        if block_name is None:
            block_key = (block.id, 0)
            block_name = block_mapping.get(block_key)

        # Use block ID as string if no mapping found
        if block_name is None:
            block_name = f"Unknown Block (ID: {block.id}, Data: {block.data})"

        # Increment counter for this block type
        if block_name in block_counts:
            block_counts[block_name] += 1
        else:
            block_counts[block_name] = 1

    return block_counts


def analyze_world_chunks(server: str, dimension: str = "overworld"):
    """
    Analyzes Minecraft world chunks for specific blocks and their counts. It processes MCA files
    to retrieve chunks, evaluates block matrices within those chunks, and calculates the count of
    specific blocks like chests, obsidian, and RF blocks. Results are categorized by location and
    summarized with total counts for each block type.

    :raises Exception: If there is an issue with loading MCA files or processing the chunks.

    :return: None
    """
    files = chunks.get_mca_files(server, dimension)
    blocks_by_location = {}

    # Process all files and chunks
    for file in files:
        chunk_list = chunks.extract_chunks_from_region_file(file)

        for chunk in chunk_list:
            # Optional filtering by chunk coordinates:
            # Earth region: 116 <= chunk.x <= 128 and -175 >= chunk.z >= -186
            # Moon region: -27 <= chunk.x <= -25 and -24 <= chunk.z <= -22

            block_list = chunks.extract_blocks_from_chunk(chunk)
            block_counts = count_blocks_in_chunk(block_list)

            if block_counts:
                chunk_key = f"x:{chunk.x*16}, z:{chunk.z*16}"
                blocks_by_location[chunk_key] = block_counts


    return blocks_by_location
