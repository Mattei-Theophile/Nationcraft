import tkinter as tk
import time
import pyautogui
from nationsglory.core import app
from nationsglory.bots.autocraft import craft, search_craft

class BaseInterface:
    """Base class for all interface screens"""
    def __init__(self, window, title, geometry="430x570"):
        self.window = window
        self.window.geometry(geometry)
        self.title = title

    def setup(self):
        """Initialize and pack all UI components"""
        self.header()
        self.body()
        self.footer()
        self.pack()

    def header(self):
        """Create header components"""
        self.label_title = tk.Label(text=self.title, font=("Arial"))

    def body(self):
        """Create body components - to be implemented by subclasses"""
        pass

    def footer(self):
        """Create footer components"""
        self.btn_back = tk.Button(
            self.window,
            text="Return to Menu",
            font=("Arial"),
            command=lambda: app.launch_application(self.window)
        )
        self.btn_logout = tk.Button(
            self.window,
            text="Logout",
            font=("Arial"),
            command=lambda: app.main()
        )

    def pack(self):
        """Pack all components - to be implemented by subclasses"""
        self.label_title.pack(side="top", fill="x", padx=5, pady=5)
        self.btn_back.pack(side="bottom", pady=5)
        self.btn_logout.pack(side="bottom", pady=5)


class ApplicationInterface(BaseInterface):
    def __init__(self, window):
        super().__init__(window, "Mr Robot")
        self.autocraft = True  # Changed from False to True to show the button

    def body(self):
        self.btn_autocraft = tk.Button(
            self.window,
            text="Autocraft",
            font=("Arial"),
            command=lambda: app.launch_auto_craft(self.window)
        )
        self.btn_automate_server = tk.Button(
            self.window,
            text="Server",
            font=("Arial"),
            command=lambda: app.launch_server(self.window)
        )
        # Commented out but preserved
        # self.btn_xray = tk.Button(self.window, text="Server", font=("Arial"), command=lambda: app.launch_xray(self.window))

    def footer(self):
        self.btn_logout = tk.Button(
            self.window,
            text="Logout",
            font=("Arial"),
            command=lambda: app.main()
        )

    def pack(self):
        self.label_title.pack(side="top", fill="x", padx=5, pady=5)
        if self.autocraft:
            self.btn_autocraft.pack(pady=5)
        self.btn_automate_server.pack(pady=5)
        self.btn_logout.pack(side="bottom", pady=5)


class AutocraftInterface(BaseInterface):
    def __init__(self, window):
        super().__init__(window, "Mr. Craft")
        self.name_id_block = tk.StringVar()
        self.one_by_one = tk.IntVar()
        self.craft_all_inventory = tk.IntVar()
        self.confidence_block = tk.DoubleVar()

    def body(self):
        # Block ID section
        self.create_block_id_section()

        # Confidence section
        self.create_confidence_section()

        # Options section
        self.create_options_section()

        # Action buttons
        self.create_action_buttons()

    def create_block_id_section(self):
        self.label_id_block = tk.Label(text="Block ID:")
        self.entry_id_block = tk.Entry(textvariable=self.name_id_block)

    def create_confidence_section(self):
        self.label_confidence_block = tk.Label(text="Block detection (0-1):")
        self.entry_confidence_block = tk.Entry(textvariable=self.confidence_block)

    def create_options_section(self):
        self.entry_one_by_one = tk.Checkbutton(
            text="One by one (64 clicks required)",
            variable=self.one_by_one
        )
        self.entry_craft_all_inventory = tk.Checkbutton(
            text="Maximum crafting",
            variable=self.craft_all_inventory
        )

    def create_action_buttons(self):
        self.btn_search_craft = tk.Button(
            self.window,
            text="Search for craft",
            font=("Arial"),
            command=self.search
        )
        self.btn_launch_craft = tk.Button(
            text="Launch crafting",
            command=self.craft
        )

    def pack(self):
        super().pack()

        # Block ID section
        self.label_id_block.pack(pady=2)
        self.entry_id_block.pack(pady=2)

        # Confidence section
        self.label_confidence_block.pack(pady=2)
        self.entry_confidence_block.pack(pady=2)

        # Options section
        self.entry_one_by_one.pack(pady=5)
        self.entry_craft_all_inventory.pack(pady=5)

        # Action buttons
        self.btn_search_craft.pack(pady=5)
        self.btn_launch_craft.pack(pady=5)

    def search(self):
        search_crafting = search_craft.SearchCrafting(self.name_id_block.get())
        time.sleep(3)
        search_crafting.open_craft()
        time.sleep(0.25)
        list_of_item = search_crafting.detect_craft()
        search_crafting.create_matrix_of_craft(list_of_item)
        search_crafting.save_craft()
        pyautogui.press("esc")

    def craft(self):
        id_block = self.name_id_block.get()
        confidence = self.confidence_block.get()
        one = self.one_by_one.get()
        all_inventory = self.craft_all_inventory.get()
        verif_matrice_of_craft = craft.verify_craft(id_block)

        if not verif_matrice_of_craft:
            print("Error! Craft not registered")
        else:
            time.sleep(3)
            crafting = craft.CraftingAutomation(one, all_inventory, confidence, id_block)
            crafting.make_craft(verif_matrice_of_craft)

        print("Craft launched!")


class ServerInterface(BaseInterface):
    def __init__(self, window):
        super().__init__(window, "Server")

    def body(self):
        self.btn_test = tk.Button(
            self.window,
            text="Test command",
            font=("Arial"),
            command=self.command_move
        )

    def pack(self):
        super().pack()
        self.btn_test.pack(pady=5)

    def command_move(self):
        # This method needs to be implemented or imported
        pass


class AutomateMoveInterface(BaseInterface):
    def __init__(self, window):
        super().__init__(window, "Automate Movement")

    def body(self):
        self.btn_test = tk.Button(
            self.window,
            text="Test command",
            font=("Arial"),
            command=self.command_move
        )

    def pack(self):
        super().pack()
        self.btn_test.pack(pady=5)

    def command_move(self):
        # This method needs to be implemented or imported
        pass