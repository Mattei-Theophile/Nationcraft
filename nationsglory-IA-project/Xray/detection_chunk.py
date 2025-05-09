import chunks
import anvil
from typing import Dict, List, Tuple, Optional

# Define constants for block IDs and their names
BLOCK_ID_NAMES = {
    3658: "server",
    54: "chest",
    146: "chest",
    3886: "rf",
    3664: "electric_meter",
    158: "dropper",
    3574: "switch",
    3575: "repair_machine",
    3576: "ecotron",
    3663: "electric_collector",
    3379: "sealable",
    2845: "heavy_wire",
    49: "obsidian",
    3657: "petroleum",
    3383: "solar_panel",
    212: "dark_ore",
    52: "spawner",
    3572: "incubator",
    7: "bedrock",
    1: "stone",
    0: None  # Air blocks to skip
}

def find_blocks_by_id(block_id: int, blocks: List[anvil.block]) -> List[Dict[str, int]]:
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
    coordinates = []
    for block in blocks:
        if block_id == block.id:
            coordinates.append({"x": block.x, "y": block.y, "z": block.z})
    return coordinates

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
        coordinates = find_blocks_by_id(block_id, chunks.get_chunk_matrice(chunk))
        results.append({(chunk.x, chunk.z): len(coordinates)})
    return results

def count_blocks_in_chunk(chunk_blocks: List[anvil.block]) -> Dict[str, int]:
    """
    Counts the occurrences of each block type in a chunk and returns a dictionary
    mapping block names to their counts. Non-air blocks are considered, and block
    names are retrieved from a global mapping. If a block name is not available
    in the mapping, the string representation of its ID is used.

    :param chunk_blocks: A list of block objects from the chunk.
    :return: A dictionary where keys are block names and values are their
             corresponding counts.
    :rtype: Dict[str, int]
    """
    block_counts = {}

    for block in chunk_blocks:
        # Skip air blocks
        if block.id == 0:
            continue

        # Get block name from the mapping or use string ID as fallback
        block_name = BLOCK_ID_NAMES.get(block.id)
        if block_name is None and block.id != 0:
            block_name = str(block.id)

        # Increment counter for this block type
        if block_name in block_counts:
            block_counts[block_name] += 1
        else:
            block_counts[block_name] = 1

    return block_counts

def analyze_world_chunks():
    """
    Analyzes Minecraft world chunks for specific blocks and their counts. It processes MCA files
    to retrieve chunks, evaluates block matrices within those chunks, and calculates the count of
    specific blocks like chests, obsidian, and RF blocks. Results are categorized by location and
    summarized with total counts for each block type.

    :raises Exception: If there is an issue with loading MCA files or processing the chunks.

    :return: None
    """
    files = chunks.get_mca_files("cyan", "")
    blocks_by_location = {}

    # Counters for summary statistics
    totals = {
        "chest": 0,
        "obsidian": 0,
        "rf": 0
    }

    # Process all files and chunks
    for file in files:
        chunk_list = chunks.get_list_of_chunks_by_mca(file)

        for chunk in chunk_list:
            # Optional filtering by chunk coordinates:
            # Earth region: 116 <= chunk.x <= 128 and -175 >= chunk.z >= -186
            # Moon region: -27 <= chunk.x <= -25 and -24 <= chunk.z <= -22

            block_list = chunks.get_chunk_matrice(chunk)
            block_counts = count_blocks_in_chunk(block_list)

            if block_counts:
                chunk_key = f"x:{chunk.x*16}, z:{chunk.z*16}"
                blocks_by_location[chunk_key] = block_counts

    # Print results and update totals
    for location, block_data in blocks_by_location.items():
        print(f"{location}: {block_data}")

        # Update totals for summary
        totals["rf"] += block_data.get("rf", 0)
        totals["obsidian"] += block_data.get("obsidian", 0)
        totals["chest"] += block_data.get("chest", 0)

    # Print summary statistics
    print(f"Total chests: {totals['chest']}")
    print(f"Total obsidian: {totals['obsidian']}")
    print(f"Total RF blocks: {totals['rf']}")

if __name__ == "__main__":
    analyze_world_chunks()