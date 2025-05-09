# Minecraft Chunk Analyzer

## Overview

Minecraft Chunk Analyzer is a powerful Python tool designed to extract, analyze, and manipulate Minecraft world data from region files (.mca). It provides utilities for exploring chunk contents, finding specific blocks, and generating schematic files for use with external tools like WorldEdit or MCEdit.

## Features

- **Find Region Files**: Locate all .mca files from a specific server and dimension
- **Extract Chunks**: Pull out all valid chunks from region files
- **Block Analysis**: Count and categorize blocks in chunks
- **Block Searching**: Find specific block types by ID
- **Schematic Generation**: Convert chunks to schematic files
- **World Analysis**: Run complete analysis of worlds to find valuable resources

## Requirements

- Python 3.9+
- Required packages:
  - anvil-parser
  - nbtschematic


## Installation

1. Clone this repository:
```shell script
git clone https://github.com/polpot/minecraft-chunk-analyzer.git
   cd minecraft-chunk-analyzer
```


2. Install required dependencies:
```shell script
pip install anvil-parser nbtschematic
```

One modification is necessary in anvil-parser program



## Command-Line Usage

The tool provides a command-line interface with multiple subcommands:

### Finding MCA Files

```shell script
python minecraft_chunk_analyzer.py find --server black --dimension overworld
```


Supported dimensions:
- overworld (default)
- lune
- mars
- edora
- edora asteroide

### Extracting Chunks from an MCA File

```shell script
python minecraft_chunk_analyzer.py extract --file path/to/region/r.0.0.mca
```


### Analyzing Blocks in a Specific Chunk

```shell script
python minecraft_chunk_analyzer.py analyze --file path/to/region/r.0.0.mca --chunk-x 5 --chunk-z -3
```


### Finding Specific Blocks by ID

```shell script
python minecraft_chunk_analyzer.py find-blocks --file path/to/region/r.0.0.mca --chunk-x 5 --chunk-z -3 --block-id 54
```


Common block IDs:
- 54: Chest
- 49: Obsidian
- 3886: RF Block
- More IDs defined in `detection_chunk.py`

### Generating a Schematic File from a Chunk

```shell script
python minecraft_chunk_analyzer.py schematic --file path/to/region/r.0.0.mca --chunk-x 5 --chunk-z -3 --output output/my_schematic.schematic
```


### Running a Full World Analysis

```shell script
python minecraft_chunk_analyzer.py world
```


## Module Structure

- **chunks.py**: Core utilities for working with region files and chunks
- **detection_chunk.py**: Functions for block detection and analysis
- **settings.py**: Path management for different operating systems
- **minecraft_chunk_analyzer.py**: Command-line interface

## Advanced Usage

### Programmatic Access

You can import the modules in your own Python code:

```python
import chunks
from detection_chunk import count_blocks_in_chunk

# Get region files
files = chunks.get_mca_files("black", "overworld")

# Process the first file
for file in files[:1]:
    chunk_list = chunks.extract_chunks_from_region_file(file)
    
    # Process each chunk
    for chunk in chunk_list:
        blocks = chunks.extract_blocks_from_chunk(chunk)
        block_counts = count_blocks_in_chunk(blocks)
        
        # Print results
        print(f"Chunk at (x:{chunk.x}, z:{chunk.z}):")
        for block_name, count in block_counts.items():
            print(f"  {block_name}: {count}")
```


### Custom Analysis

You can define your own analysis functions by using the provided modules as a foundation:

```python
def find_valuable_chunks(server, dimension, valuable_block_ids):
    """Find chunks containing valuable blocks."""
    files = chunks.get_mca_files(server, dimension)
    valuable_chunks = []
    
    for file in files:
        chunk_list = chunks.extract_chunks_from_region_file(file)
        for chunk in chunk_list:
            blocks = chunks.extract_blocks_from_chunk(chunk)
            for block_id in valuable_block_ids:
                if any(block.id == block_id for block in blocks):
                    valuable_chunks.append((chunk.x, chunk.z))
                    break
                    
    return valuable_chunks
```


## Limitations

- The tool is designed for Minecraft Java Edition
- Large worlds may require significant processing time
- Currently no support for block entity data (chest contents, etc.)

## Troubleshooting

### Common Issues

1. **Path not found**: Make sure your NationsGlory installation path is correct in `settings.py`
2. **Missing dependencies**: Ensure you've installed all required packages
3. **Memory errors**: For very large worlds, you may need to process chunks in batches

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The anvil-parser and nbtschematic libraries for making Minecraft data accessible in Python

---

*This tool is not affiliated with Mojang or Microsoft.*