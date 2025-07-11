import streamlit as st

from nationsglory.bots.xray.detection_chunk import analyze_world_chunks, load_block_id, find_blocks_by_id
from nationsglory.bots.xray import chunks
import anvil

# Main page content
st.markdown("# Xray 🔎")
st.sidebar.markdown("# Xray 🔎")



analyser, findBlock, schematic = st.tabs(["Analyser un serveur", "Recherche", "Schematic"])
st.session_state.list_block_xray = []
st.session_state.list_block_xray_by_block_id = []


with analyser:

    server = st.selectbox("Choisissez un serveur", ["blue","orange", "yellow", "white", "black", "cyan","lime","coral","pink","purple","green","red", "mocha"])
    dimension = st.selectbox("Choisissez une dimension", ["Overworld", "Lune", "Mars", "Edora", "Edora asteroide"])
    st.spinner("Analyse en cours...")
    if st.button("Analyser un serveur"):
        st.session_state.xray_data = analyze_world_chunks(server, dimension)
        analyser.dataframe(st.session_state.xray_data)

with findBlock:
    blocks_to_find = {}

    xrayFile = findBlock.file_uploader("Choisissez un fichier MCA", type="mca")
    if xrayFile:
        list_of_coordinates_chunks = anvil.Region(xrayFile).get_chunk_coordinates()
        st.write(f"Nombre de chunks : {len(list_of_coordinates_chunks)}")
        st.write(f"chunks : {list_of_coordinates_chunks}")


    blocks = st.popover("blocks")


    for block in load_block_id():
        key = [block["item_id"], block["metadata"], block["name"]]
        # Store both the checkbox state and its key
        checkbox_state = blocks.checkbox(block["name"], key=f"block_{block['item_id']}_{block['metadata']}")
        if checkbox_state:
            st.session_state.list_block_xray.append(key)


    chunkContainer1, chunkContainer2, chunkContainer3 = st.columns(3, vertical_alignment="center")

    chunkContainer1.write("Choisissez un chunk :")
    chunk_x = chunkContainer2.number_input("X_blocks", min_value=0, max_value=31, value=0)
    chunk_z = chunkContainer3.number_input("Z_blocks", min_value=0, max_value=31, value=0)


    if st.button("Rechercher des blocs"):
        st.success("Recherche en cours...")
        region = anvil.Region.from_file(xrayFile)

        chunk = region.get_chunk(chunk_x, chunk_z)
        block_list = chunks.extract_blocks_from_chunk(chunk)

        for block_key in st.session_state.list_block_xray:
            st.session_state.list_block_xray_by_block_id.append([block_key[3],find_blocks_by_id(block_key[0], block_key[1],block_list)])
        st.dataframe(st.session_state.list_block_xray_by_block_id)

with schematic:
    schematicFile = schematic.file_uploader("Choisissez un fichier pour créer un schematic", type="mca")
    chunkContainer1,chunkContainer2,chunkContainer3 = st.columns(3, vertical_alignment="center")

    chunkContainer1.write("Choisissez un chunk :")
    chunk_x = chunkContainer2.number_input("X", min_value=0, max_value=31, value=0)
    chunk_z = chunkContainer3.number_input("Z", min_value=0, max_value=31, value=0)

    if st.button("Créer un schematic"):
        region = anvil.Region.from_file(schematicFile)
        chunk = region.get_chunk(chunk_x, chunk_z)
        block_list = chunks.extract_blocks_from_chunk(chunk)


        # Generate the schematic file
        schematic = chunks.save_chunks_as_schematic([block_list])

        st.download_button(
            label="Télécharger le schematic",
            data=schematic,
            file_name=f"{xrayFile.name[:-4]}.schematic",
            mime="text/schematic",
            icon=":material/download:",
        )




