#!/usr/bin/env python3
"""
Minecraft Chunk Analyzer - Command Line Interface
"""
import os
import argparse
import chunks
from detection_chunk import count_blocks_in_chunk, find_blocks_by_id, BLOCK_ID_NAMES, analyze_world_chunks

def main():
    parser = argparse.ArgumentParser(description="Analyze Minecraft chunks and regions")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Find MCA files command
    find_parser = subparsers.add_parser("find", help="Find MCA files")
    find_parser.add_argument("--server", required=True, help="Server name")
    find_parser.add_argument("--dimension", default="overworld",
                             choices=["overworld", "lune", "mars", "edora", "edora asteroide"],
                             help="Dimension name")

    # Extract chunks command
    extract_parser = subparsers.add_parser("extract", help="Extract chunks from MCA file")
    extract_parser.add_argument("--file", required=True, help="Path to MCA file")

    # Analyze blocks command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze blocks in a chunk")
    analyze_parser.add_argument("--file", required=True, help="Path to MCA file")
    analyze_parser.add_argument("--chunk-x", type=int, required=True, help="Chunk X coordinate")
    analyze_parser.add_argument("--chunk-z", type=int, required=True, help="Chunk Z coordinate")

    # Find blocks command
    find_blocks_parser = subparsers.add_parser("find-blocks", help="Find specific blocks")
    find_blocks_parser.add_argument("--file", required=True, help="Path to MCA file")
    find_blocks_parser.add_argument("--chunk-x", type=int, required=True, help="Chunk X coordinate")
    find_blocks_parser.add_argument("--chunk-z", type=int, required=True, help="Chunk Z coordinate")
    find_blocks_parser.add_argument("--block-id", type=int, required=True, help="Block ID to find")

    # Generate schematic command
    schematic_parser = subparsers.add_parser("schematic", help="Generate schematic from chunk")
    schematic_parser.add_argument("--file", required=True, help="Path to MCA file")
    schematic_parser.add_argument("--chunk-x", type=int, required=True, help="Chunk X coordinate")
    schematic_parser.add_argument("--chunk-z", type=int, required=True, help="Chunk Z coordinate")
    schematic_parser.add_argument("--output", required=True, help="Output path for schematic file")

    # Full world analysis command
    world_parser = subparsers.add_parser("world", help="Run full world analysis")

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if args.command == "find":
        files = chunks.get_mca_files(args.server, args.dimension)
        print(f"Found {len(files)} MCA files:")
        for i, file in enumerate(files[:20]):
            print(f"{i+1}. {os.path.basename(file)}")
        if len(files) > 20:
            print(f"...and {len(files) - 20} more files")

    elif args.command == "extract":
        chunk_list = chunks.extract_chunks_from_region_file(args.file)
        print(f"Found {len(chunk_list)} chunks in {os.path.basename(args.file)}")
        for i, chunk in enumerate(chunk_list[:10]):
            print(f"{i+1}. Chunk at (x:{chunk.x}, z:{chunk.z})")

    elif args.command == "analyze":
        region = anvil.Region.from_file(args.file)
        chunk = region.get_chunk(args.chunk_x, args.chunk_z)
        block_list = chunks.extract_blocks_from_chunk(chunk)
        block_counts = count_blocks_in_chunk(block_list)

        print(f"Block counts for chunk (x:{args.chunk_x}, z:{args.chunk_z}):")
        for block_name, count in sorted(block_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{block_name}: {count}")

    elif args.command == "find-blocks":
        region = anvil.Region.from_file(args.file)
        chunk = region.get_chunk(args.chunk_x, args.chunk_z)
        block_list = chunks.extract_blocks_from_chunk(chunk)

        block_name = BLOCK_ID_NAMES.get(args.block_id, f"Unknown (ID: {args.block_id})")
        found_blocks = find_blocks_by_id(args.block_id, block_list)

        print(f"Found {len(found_blocks)} instances of {block_name} in chunk (x:{args.chunk_x}, z:{args.chunk_z})")
        for i, block in enumerate(found_blocks[:20]):
            print(f"{i+1}. Position: (x:{block['x']}, y:{block['y']}, z:{block['z']})")

    elif args.command == "schematic":
        region = anvil.Region.from_file(args.file)
        chunk = region.get_chunk(args.chunk_x, args.chunk_z)
        block_list = chunks.extract_blocks_from_chunk(chunk)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

        # Generate the schematic file
        chunks.save_chunks_as_schematic([block_list], args.output)
        print(f"Schematic file generated successfully at {args.output}")

    elif args.command == "world":
        print("Running full world analysis (this may take a while)...")
        analyze_world_chunks()
        print("Analysis complete!")

    else:
        parser.print_help()


main()