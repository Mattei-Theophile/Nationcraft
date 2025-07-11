import streamlit as st
import time
import json
import os
from nationsglory.bots.player.bots import player_bot

# Main page content
st.markdown("# Bot 🤖")
st.sidebar.markdown("# Bot 🤖")

st.markdown("## Player Bot")
st.markdown("Control your Minecraft character with automated actions")

# Create columns for different actions
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movement Controls")

    # Helper function to record movement
    def record_movement(action, **params):
        player_bot.record_movement(action, **params)

    if st.button("Move Forward"):
        player_bot.move("forward")
        record_movement('move', direction='forward', blocks=1)

    if st.button("Move Backward"):
        player_bot.move("back")
        record_movement('move', direction='back', blocks=1)

    if st.button("Move Left"):
        player_bot.move("left")
        record_movement('move', direction='left', blocks=1)

    if st.button("Move Right"):
        player_bot.move("right")
        record_movement('move', direction='right', blocks=1)

    # Add block count for movements
    blocks = st.number_input("Blocks to move", min_value=1, max_value=10, value=1)

    if st.button("Move Forward (Custom)"):
        player_bot.move("forward", blocks)
        record_movement('move', direction='forward', blocks=blocks)

    if st.button("Jump"):
        player_bot.jump()
        record_movement('jump')

    if st.button("Sneak"):
        player_bot.sneak()
        record_movement('sneak')

with col2:
    st.subheader("Actions")
    if st.button("Use Item/Block"):
        player_bot.use()
        record_movement('use')

    if st.button("Attack/Break"):
        player_bot.attack()
        record_movement('attack')

    if st.button("Open Inventory"):
        player_bot.inventory()
        record_movement('inventory')

    st.subheader("Chat")
    message = st.text_input("Enter message:")
    if st.button("Send Message") and message:
        player_bot.write(message)
        record_movement('chat', message=message)

# Automated tasks
st.subheader("Automated Tasks")
task_col1, task_col2 = st.columns(2)

with task_col1:
    if st.toggle("Anti-AFK"):
        if player_bot.is_anti_afk_running:
            player_bot.anti_afk(False)
            st.success("Anti-AFK disabled")
        else:
            player_bot.anti_afk(True)
            st.success("Anti-AFK enabled")

    if st.toggle("Discord Chat"):
        if player_bot.is_discord_chat_running:
            player_bot.discord_chat(False)
            st.success("Discord chat disabled")
        else:
            player_bot.discord_chat(True)
            st.success("Discord chat enabled")

with task_col2:
    task_duration = st.slider("Task Duration (seconds)", 10, 300, 60)

    if st.button("Auto Farm"):
        player_bot.auto_farm(task_duration)
        st.success(f"Auto farming completed for {task_duration} seconds")

    if st.button("Auto Mine"):
        player_bot.auto_mine(task_duration)
        st.success(f"Auto mining completed for {task_duration} seconds")



    # Auto Mine Chunk section
    st.subheader("Auto Mine Chunk")
    chunk_col1, chunk_col2 = st.columns(2)

    with chunk_col1:
        chunk_height = st.number_input("Height (layers)", min_value=1, max_value=20, value=3)

    with chunk_col2:
        mining_speed = st.number_input("Mining Speed", min_value=0.1, max_value=2.0, value=0.5, step=0.1,
                                      help="Lower values = faster mining (seconds between actions)")

    if st.button("Mine Chunk"):
        result = player_bot.auto_mine_chunk(height=chunk_height, mining_speed=mining_speed)
        if result:
            st.success(f"Chunk mining completed successfully! Mined {chunk_height} layers.")
        else:
            st.error("Error during chunk mining. Check the console for details.")

# Movement Schema System
st.subheader("Movement Schema")
schema_tab1, schema_tab2 = st.tabs(["Record & Save", "Load & Execute"])

# Initialize session state variables for schema display
if 'show_schema' not in st.session_state:
    st.session_state.show_schema = False

with schema_tab1:
    st.write("Record a sequence of movements and save it as a schema")

    # Recording controls
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Recording"):
            player_bot.start_recording()
            st.success("Recording started. Use the movement controls above.")

        if st.button("Stop Recording"):
            movements_count = player_bot.stop_recording()
            st.success(f"Recording stopped. {movements_count} movements recorded.")
            st.session_state.show_schema = True

    with col2:
        schema_name = st.text_input("Schema Name", placeholder="my_schema")

        if st.button("Save Schema") and schema_name:
            schema_path = player_bot.save_schema(schema_name)
            if schema_path:
                st.success(f"Schema saved to {schema_path}")
            else:
                st.error("Error saving schema. Make sure you have recorded some movements.")

    # Display current schema
    if st.session_state.show_schema:
        st.write("Current Schema:")
        st.json(player_bot.current_schema)

    # Recording status
    if player_bot.recording:
        st.warning("Recording in progress... Use the movement controls above.")

with schema_tab2:
    st.write("Load and execute saved movement schemas")

    # Get list of available schemas
    available_schemas = player_bot.get_available_schemas()

    if available_schemas:
        selected_schema = st.selectbox("Select Schema", [f"{schema}.json" for schema in available_schemas])
        schema_name = selected_schema.split('.')[0]  # Remove .json extension

        if st.button("Load Schema"):
            try:
                movements_count = player_bot.load_schema(schema_name)
                if movements_count:
                    st.success(f"Schema loaded: {movements_count} movements")
                    st.session_state.show_schema = True
                else:
                    st.error("Error loading schema.")
            except Exception as e:
                st.error(f"Error loading schema: {str(e)}")

        if st.button("Execute Schema"):
            try:
                if player_bot.execute_schema():
                    st.success("Schema executed successfully")
                else:
                    st.error("Error executing schema. Make sure a schema is loaded.")
            except Exception as e:
                st.error(f"Error executing schema: {str(e)}")

        # Display current schema
        if st.session_state.show_schema:
            st.write("Current Schema:")
            st.json(player_bot.current_schema)
    else:
        st.info("No saved schemas found. Record and save a schema first.")
