import streamlit as st
import time
st.set_page_config(page_title="NationsGlory Helper", page_icon=":robot:")
st.write("# NationsGlory Helper")



# Constants for page paths and icons
PAGE_PATHS = {
    "launcher": "pages/launcher.py",
    "bot": "pages/bot.py",
    "xray": "pages/xray.py",
    "autocraft": "pages/autocraft.py",
    "trading": "pages/trading.py",
    "schematica": "pages/schematica.py"
}

ICONS = {
    "launcher": "💻",
    "bot": "🤖",
    "xray": "🔎",
    "autocraft": "⚒️",
    "trading": "🏦",
    "schematica": "🏗️"
}

def create_page(name):
    """Create a streamlit page with consistent formatting."""
    return st.Page(
        PAGE_PATHS[name],
        title=name.capitalize(),
        icon=ICONS[name]
    )

# Create all pages
pages = [create_page(name) for name in PAGE_PATHS.keys()]
pages = st.navigation(pages)

# Run the selected page
pages.run()
