# NationsGlory Helper

A comprehensive tool for automating tasks in the Minecraft NationsGlory server. This application provides various utilities to enhance your gameplay experience through automation and helpful tools.

## Features

- **Launcher**: Easy game launching and configuration
- **Bot**: General bot functionality for automation
- **Xray Detection**: Tools for detecting and analyzing xray patterns
- **Autocraft**: Automated crafting system
- **Trading**: Trading assistance and automation
- **Schematica**: Building from schematic files

## Installation

### Prerequisites

- Python 3.6 or higher
- Minecraft with NationsGlory server access

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nationsglory.git
   cd nationsglory
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install the package:
   ```
   pip install -e .
   ```

## Usage

### Running the Streamlit App

```
streamlit run app.py
```

This will launch the web interface where you can access all the features.

### Command Line Usage

```
nationsglory
```

## Dependencies

- nbtschematic: For Minecraft schematic files
- PyAutoGUI and PyGetWindow: For GUI automation
- NBT: For Minecraft's NBT file format
- numpy, opencv-python, pytesseract: For image processing and OCR
- matplotlib, pillow: For image manipulation and visualization
- streamlit: For the web interface

## Project Structure

- **anvil/**: Minecraft Anvil file format utilities
- **nationsglory/**: Main project directory
  - **bots/**: Automation bots
  - **assets/**: Images and resources
  - **config/**: Configuration files
  - **core/**: Core functionality
  - **utils/**: Utility functions
- **pages/**: Streamlit pages for the web interface
- **movements_schema/**: Movement patterns and schemas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use at your own risk and in accordance with the NationsGlory server rules.