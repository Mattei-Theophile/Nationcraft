"""
NationsGlory Bot - Main Entry Point

This module serves as the main entry point for the NationsGlory Bot application.
It imports and runs the application from the core module.
"""

from nationsglory.core.app import main
from nationsglory.utils.IDs import parse_nationsgui_hdv_mappings, save_hdv_mappings_to_file, display_hdv_mappings

if __name__ == "__main__":
    mappings = parse_nationsgui_hdv_mappings()
    save_hdv_mappings_to_file(mappings)
    display_hdv_mappings(mappings)
    main()