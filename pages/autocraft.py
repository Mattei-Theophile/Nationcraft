import streamlit as st
from nationsglory.bots.xray.detection_chunk import load_block_id
from nationsglory.bots.autocraft.craft import CraftingAutomation, verify_craft
# Main page content
st.markdown("# AutoCraft ⚒️")
st.sidebar.markdown("# AutoCraft ⚒️")

st.write("Créer ton craft dans le tableau")

craftingTable, blockList = st.columns(2, vertical_alignment="top")
st.session_state.list_craft = []

# Create a 3x3 crafting grid
row1 = craftingTable.columns(3)
row2 = craftingTable.columns(3)
row3 = craftingTable.columns(3)

# Initialize crafting matrix if not already in session state
if 'crafting_matrix' not in st.session_state:
    st.session_state.crafting_matrix = [["", "", ""], ["", "", ""], ["", "", ""]]

# Create the crafting grid UI
for i, row in enumerate([row1, row2, row3]):
    for j, col in enumerate(row):
        tile = col.container(height=120)
        block_name = tile.text_input("Nom du bloc", 
                                    value=st.session_state.crafting_matrix[i][j], 
                                    key=f"craft_{i}_{j}")
        st.session_state.crafting_matrix[i][j] = block_name
        st.session_state.list_craft.append(block_name)

# Crafting options
craft_options = craftingTable.expander("Options de craft", expanded=True)
st.session_state.craft_number = craft_options.number_input("Nombre de craft", min_value=1, max_value=64, value=1)
one_by_one = craft_options.checkbox("Crafter un par un", value=False)
craft_all = craft_options.checkbox("Utiliser tout l'inventaire", value=False)
confidence = craft_options.slider("Confiance de détection", min_value=0.1, max_value=1.0, value=0.8, step=0.1)

# Execute craft button
if craftingTable.button("Éxecuter le craft"):
    # Get the block ID from the first non-empty block in the crafting matrix
    block_id = None
    for row in st.session_state.crafting_matrix:
        for block in row:
            if block:
                block_id = block
                break
        if block_id:
            break

    if block_id:
        # Verify if the craft exists
        recipe = verify_craft(block_id)
        if recipe:
            # Create crafting automation instance
            crafter = CraftingAutomation(
                one_by_one=one_by_one,
                craft_all_inventory=craft_all,
                confidence_of_block=confidence,
                id_block=block_id
            )

            # Execute the craft
            try:
                crafter.make_craft(st.session_state.crafting_matrix)
                craftingTable.success(f"Craft exécuté avec succès! ({st.session_state.craft_number} fois)")
            except Exception as e:
                craftingTable.error(f"Erreur lors du craft: {str(e)}")
        else:
            craftingTable.warning(f"Recette de craft non trouvée pour {block_id}")
    else:
        craftingTable.error("Veuillez spécifier au moins un bloc dans la grille de craft")

# Block list
blockList.title("Liste des blocs")
blocks_data = load_block_id()
blockList.table(blocks_data)

# Search functionality
search_term = blockList.text_input("Rechercher un bloc:")
if search_term:
    filtered_blocks = [block for block in blocks_data if search_term.lower() in block["name"].lower()]
    blockList.write(f"{len(filtered_blocks)} blocs trouvés:")
    blockList.table(filtered_blocks)

# Save/Load crafting recipes
recipe_col1, recipe_col2 = craftingTable.columns(2)
recipe_name = recipe_col1.text_input("Nom de la recette:")

if recipe_col1.button("Sauvegarder la recette") and recipe_name:
    # Get the block ID from the first non-empty block in the crafting matrix
    block_id = None
    for row in st.session_state.crafting_matrix:
        for block in row:
            if block:
                block_id = block
                break
        if block_id:
            break

    if block_id:
        # Save the recipe
        if CraftingAutomation.save_craft(recipe_name, block_id, st.session_state.crafting_matrix):
            craftingTable.success(f"Recette '{recipe_name}' sauvegardée!")
        else:
            craftingTable.error("Erreur lors de la sauvegarde de la recette.")
    else:
        craftingTable.error("Veuillez spécifier au moins un bloc dans la grille de craft.")

# Get available recipes
available_recipes = CraftingAutomation.get_available_crafts()
selected_recipe = recipe_col2.selectbox("Charger une recette:", [""] + available_recipes)

if recipe_col2.button("Charger la recette") and selected_recipe:
    # Load the recipe
    recipe = CraftingAutomation.load_craft(selected_recipe)
    if recipe:
        # Update the crafting matrix
        st.session_state.crafting_matrix = recipe["matrix"]
        craftingTable.success(f"Recette '{selected_recipe}' chargée!")

    else:
        craftingTable.error(f"Erreur lors du chargement de la recette '{selected_recipe}'.")
