import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from nationsglory.bots.schematica.schematica_bot import SchematicaBot
from nationsglory.config import settings

# Main page content
st.markdown("# Schematica 🏗️")
st.sidebar.markdown("# Schematica 🏗️")

# Initialize session state variables if they don't exist
if 'current_schematic' not in st.session_state:
    st.session_state.current_schematic = None
if 'current_layer' not in st.session_state:
    st.session_state.current_layer = 0

# Create tabs for different functionalities
load_tab, view_tab, build_tab = st.tabs(["Load Schematic", "View Schematic", "Build Schematic"])

# Function to display a layer of the schematic as a heatmap
def display_layer(layer):
    if layer.size == 0:
        st.warning("No layer data available")
        return
    
    # Create a colormap for the blocks
    # This is a simplified approach; in a real implementation, you would map block IDs to actual colors
    cmap = plt.cm.get_cmap('viridis', 256)
    
    # Create the figure and plot
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(layer, cmap=cmap)
    
    # Add a colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Block ID')
    
    # Set the title and labels
    ax.set_title(f'Layer {st.session_state.current_layer}')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    
    # Display the plot
    st.pyplot(fig)

# Load Schematic tab
with load_tab:
    st.header("Load a Schematic")
    
    # Option to upload a schematic file
    uploaded_file = st.file_uploader("Upload a schematic file", type=["schematic"])
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_path = os.path.join(settings.PathGestion().get_ng_dir(), "temp", uploaded_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load the schematic
        if SchematicaBot.load_schematic_file(temp_path):
            st.session_state.current_schematic = SchematicaBot.current_schematic
            st.success(f"Schematic '{uploaded_file.name}' loaded successfully!")
        else:
            st.error("Failed to load schematic file")
    
    # Option to select an existing schematic
    st.header("Or select an existing schematic")
    available_schematics = SchematicaBot.get_available_schematics()
    
    if available_schematics:
        selected_schematic = st.selectbox("Select a schematic", available_schematics)
        
        if st.button("Load Selected Schematic"):
            schematic_path = os.path.join(SchematicaBot.schematic_dir, f"{selected_schematic}.schematic")
            if SchematicaBot.load_schematic_file(schematic_path):
                st.session_state.current_schematic = SchematicaBot.current_schematic
                st.success(f"Schematic '{selected_schematic}' loaded successfully!")
            else:
                st.error("Failed to load schematic file")
    else:
        st.info("No schematics available. Upload a schematic file to get started.")

# View Schematic tab
with view_tab:
    st.header("View Schematic")
    
    if st.session_state.current_schematic is not None:
        # Display schematic information
        info = SchematicaBot.get_schematic_info()
        st.subheader("Schematic Information")
        st.write(f"Name: {info['name']}")
        st.write(f"Dimensions: {info['dimensions']['height']} x {info['dimensions']['width']} x {info['dimensions']['length']} (H x W x L)")
        st.write(f"Total Blocks: {info['total_blocks']}")
        
        # Display block counts
        st.subheader("Block Counts")
        block_counts = info['block_counts']
        if block_counts:
            # Convert block counts to a format suitable for display
            block_data = []
            for block_id, count in block_counts.items():
                if block_id > 0:  # Skip air blocks
                    block_data.append({"Block ID": block_id, "Count": count})
            
            if block_data:
                st.dataframe(block_data)
            else:
                st.info("No blocks found in the schematic")
        else:
            st.info("No block count information available")
        
        # Layer viewer
        st.subheader("Layer Viewer")
        max_layer = info['dimensions']['height'] - 1
        st.session_state.current_layer = st.slider("Select Layer", 0, max_layer, st.session_state.current_layer)
        
        # Display the selected layer
        layer = SchematicaBot.get_layer(st.session_state.current_layer)
        display_layer(layer)
    else:
        st.info("No schematic loaded. Go to the 'Load Schematic' tab to load a schematic.")

# Build Schematic tab
with build_tab:
    st.header("Build Schematic")
    
    if st.session_state.current_schematic is not None:
        # Display schematic information
        info = SchematicaBot.get_schematic_info()
        st.subheader("Schematic Information")
        st.write(f"Name: {info['name']}")
        st.write(f"Dimensions: {info['dimensions']['height']} x {info['dimensions']['width']} x {info['dimensions']['length']} (H x W x L)")
        
        # Layer selection for building
        st.subheader("Build Options")
        max_layer = info['dimensions']['height'] - 1
        start_layer = st.number_input("Start Layer", 0, max_layer, 0)
        end_layer = st.number_input("End Layer", start_layer, max_layer, max_layer)
        
        # Build button
        if st.button("Build Schematic"):
            with st.spinner("Building schematic..."):
                success = SchematicaBot.build_schematic(start_layer, end_layer)
                if success:
                    st.success("Schematic built successfully!")
                else:
                    st.error("Failed to build schematic")
    else:
        st.info("No schematic loaded. Go to the 'Load Schematic' tab to load a schematic.")