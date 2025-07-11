import time
import pyautogui
import sys
import os
import subprocess
import json
from nationsglory.utils.keycode import KeycodeManager

class Player:
    def __init__(self):
        self.os_sys = sys.platform
        self.ng_dir = self.get_ng_dir()
        self.keycode_manager = KeycodeManager(self.ng_dir)
        self.key_control = self.keycode_manager.link_key_control()
        self.x = 0
        self.y = 0
        self.speed = 0.231
        self.is_anti_afk_running = False
        self.is_discord_chat_running = False

        # Schema recording variables
        self.recording = False
        self.current_schema = []
        self.schemas_dir = os.path.join("movements_schema")
        os.makedirs(self.schemas_dir, exist_ok=True)

    def get_ng_dir(self):
        """Get the NationsGlory directory path based on the operating system"""
        ng_path = None
        match self.os_sys:
            case "win32":
                ng_path = os.getenv("APPDATA")
                ng_path = os.path.join(ng_path, ".NationsGlory")
            case "linux":
                subprocess.run(["xhost +"], shell=True)
                ng_path = f"/home/{os.getlogin()}/.config/.NationsGlory"
        return ng_path

    def inventory(self):
        """Open the inventory"""
        pyautogui.press(self.key_control["key_key.inventory"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('inventory')

    def move(self, direction, block=1):
        """Move the player in the specified direction for a number of blocks"""
        wait_time = self.speed * block
        match direction:
            case "forward":
                pyautogui.keyDown(self.key_control["key_key.forward"])
                time.sleep(wait_time)
                pyautogui.keyUp(self.key_control["key_key.forward"])
            case "back":
                pyautogui.keyDown(self.key_control["key_key.back"])
                time.sleep(wait_time)
                pyautogui.keyUp(self.key_control["key_key.back"])
            case "left":
                pyautogui.keyDown(self.key_control["key_key.left"])
                time.sleep(wait_time)
                pyautogui.keyUp(self.key_control["key_key.left"])
            case "right":
                pyautogui.keyDown(self.key_control["key_key.right"])
                time.sleep(wait_time)
                pyautogui.keyUp(self.key_control["key_key.right"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('move', direction=direction, blocks=block)

    def jump(self):
        """Make the player jump"""
        pyautogui.keyDown(self.key_control["key_key.jump"])
        pyautogui.keyUp(self.key_control["key_key.jump"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('jump')

    def sneak(self):
        """Toggle sneak mode"""
        pyautogui.press(self.key_control["key_key.sneak"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('sneak')

    def use(self):
        """Use the item in hand or interact with a block"""
        pyautogui.rightClick()

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('use')

    def attack(self):
        """Attack or break a block"""
        pyautogui.leftClick()

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('attack')

    def destroy(self):
        """Alternative way to break a block"""
        pyautogui.press(self.key_control["key_key.attack"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('destroy')

    def open_chat(self):
        """Open the chat window"""
        pyautogui.press(self.key_control["key_key.chat"])

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('open_chat')

    def write(self, message):
        """Write a message in the chat and send it"""
        self.open_chat()
        pyautogui.write(message)
        pyautogui.press("enter")

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('chat', message=message)

    def head(self, horizontal, vertical):
        """Move the player's head to look in a direction"""
        pyautogui.moveTo(x=vertical, y=horizontal, duration=0.5)

        # Record the movement if recording is enabled
        if self.recording:
            self.record_movement('head', horizontal=horizontal, vertical=vertical)

    def anti_afk(self, enabled=True):
        """Toggle anti-AFK mode"""
        self.is_anti_afk_running = enabled
        if enabled:
            # This would be implemented as a separate thread in a real application
            print("Anti-AFK mode enabled")
        else:
            print("Anti-AFK mode disabled")

    def discord_chat(self, enabled=True):
        """Toggle Discord chat integration"""
        self.is_discord_chat_running = enabled
        if enabled:
            # This would be implemented as a separate thread in a real application
            print("Discord chat integration enabled")
        else:
            print("Discord chat integration disabled")

    def auto_farm(self, duration=60):
        """Automatically farm by moving forward and breaking blocks"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.move("forward", 1)
            self.attack()
            time.sleep(0.5)

    def auto_mine(self, duration=60):
        """Automatically mine by moving forward and breaking blocks"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.attack()
            time.sleep(1)
            self.move("forward", 1)
            time.sleep(0.5)



    def auto_mine_chunk(self, height=3, mining_speed=0.5):
        """
        Automatically mine a 16x16 chunk up to the specified height.

        This method systematically mines blocks in a snake pattern to cover a 16x16 area (a chunk),
        and repeats this pattern for each layer up to the specified height. The player should be
        positioned at one corner of the chunk before calling this method.

        Parameters
        ----------
        height : int
            The height to mine up to (number of layers)
        mining_speed : float
            The delay in seconds between mining actions (lower values = faster mining)

        Notes
        -----
        - The player should be positioned at one corner of the chunk before calling this method
        - The method uses teleport commands to move between layers, which requires appropriate permissions
        - The method assumes a clear path for mining without obstacles
        """
        # Validate parameters
        if height <= 0:
            print("Error: Height must be greater than 0")
            return False

        if mining_speed <= 0:
            print("Error: Mining speed must be greater than 0")
            return False

        try:
            # Mine in a systematic pattern to cover a 16x16 area
            for layer in range(height):
                print(f"Mining layer {layer+1} of {height}...")
                # Start at one corner of the chunk
                for row in range(16):
                    # Mine 16 blocks in a row
                    for col in range(15):
                        self.attack()
                        time.sleep(mining_speed)
                        self.move("forward", 1)
                        time.sleep(mining_speed * 0.4)  # Shorter delay for movement

                    # Mine the last block in the row
                    self.attack()
                    time.sleep(mining_speed)

                    # Turn to the next row (alternate directions to create a snake pattern)
                    if row < 15:  # Don't turn after the last row
                        if row % 2 == 0:
                            # Turn right at the end of even rows
                            self.move("right", 1)
                            time.sleep(mining_speed * 0.4)
                            self.move("forward", 1)
                            time.sleep(mining_speed * 0.4)
                            self.move("right", 1)
                            time.sleep(mining_speed * 0.4)
                        else:
                            # Turn left at the end of odd rows
                            self.move("left", 1)
                            time.sleep(mining_speed * 0.4)
                            self.move("forward", 1)
                            time.sleep(mining_speed * 0.4)
                            self.move("left", 1)
                            time.sleep(mining_speed * 0.4)

                # After completing a layer, move up to the next layer if not at the top
                if layer < height - 1:
                    print(f"Moving up to layer {layer+2}...")
                    # Move to a position where the player can safely move up
                    # This could be a staircase or ladder that the player has prepared

                    # Option 1: Use a prepared staircase
                    # Move to the staircase position
                    self.write("/tp @s ~0 ~1 ~0")  # Use a command to teleport up one block
                    time.sleep(1)

                    # Option 2: If commands are not available, try to use blocks to build up
                    # This would require the player to have blocks in their inventory
                    # self.inventory()
                    # time.sleep(0.5)
                    # Select a block from inventory (would need to be implemented)
                    # Place the block and jump on it

                    # Reset position to the starting corner for the next layer
                    # This would depend on the specific layout of the mining area
                    # For now, we assume the player can navigate back to the starting position

                print(f"Completed layer {layer+1} of {height}")

            print("Mining completed successfully!")
            return True
        except Exception as e:
            print(f"Error during mining: {str(e)}")
            return False



    # Schema recording methods
    def start_recording(self):
        """Start recording a movement schema"""
        self.recording = True
        self.current_schema = []
        return True

    def stop_recording(self):
        """Stop recording a movement schema"""
        self.recording = False
        return len(self.current_schema)

    def record_movement(self, action, **params):
        """Record a movement or action in the current schema"""
        if self.recording:
            movement = {'action': action, 'params': params}
            self.current_schema.append(movement)
            return True
        return False

    def save_schema(self, schema_name):
        """Save the current schema to a file"""
        if not self.current_schema:
            return False

        schema_path = os.path.join(self.schemas_dir, f"{schema_name}.json")
        try:
            with open(schema_path, 'w') as f:
                json.dump(self.current_schema, f)
            return schema_path
        except Exception as e:
            print(f"Error saving schema: {str(e)}")
            return False

    def load_schema(self, schema_name):
        """Load a schema from a file"""
        schema_path = os.path.join(self.schemas_dir, f"{schema_name}.json")
        try:
            with open(schema_path, 'r') as f:
                self.current_schema = json.load(f)
            return len(self.current_schema)
        except Exception as e:
            print(f"Error loading schema: {str(e)}")
            return False

    def execute_schema(self):
        """Execute the current schema"""
        if not self.current_schema:
            return False

        try:
            for movement in self.current_schema:
                action = movement['action']
                params = movement.get('params', {})

                if action == 'move':
                    direction = params.get('direction', 'forward')
                    blocks = params.get('blocks', 1)
                    self.move(direction, blocks)
                elif action == 'jump':
                    self.jump()
                elif action == 'sneak':
                    self.sneak()
                elif action == 'use':
                    self.use()
                elif action == 'attack':
                    self.attack()
                elif action == 'destroy':
                    self.destroy()
                elif action == 'inventory':
                    self.inventory()
                elif action == 'open_chat':
                    self.open_chat()
                elif action == 'chat':
                    message = params.get('message', '')
                    if message:
                        self.write(message)
                elif action == 'head':
                    horizontal = params.get('horizontal', 0)
                    vertical = params.get('vertical', 0)
                    self.head(horizontal, vertical)

                # Add a small delay between actions
                time.sleep(0.1)

            return True
        except Exception as e:
            print(f"Error executing schema: {str(e)}")
            return False

    def get_available_schemas(self):
        """Get a list of available schemas"""
        try:
            return [f[:-5] for f in os.listdir(self.schemas_dir) if f.endswith('.json')]
        except Exception as e:
            print(f"Error getting schemas: {str(e)}")
            return []

# Create a singleton instance
player_bot = Player()
