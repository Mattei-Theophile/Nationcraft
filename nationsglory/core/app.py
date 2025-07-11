import tkinter as tk
from nationsglory.utils import window_utils
import streamlit as st

def setup_interface(window, interface_class):
    """
    Set up a generic interface with standard components.
    
    Args:
        window: The tkinter window
        interface_class: The interface class to instantiate
        
    Returns:
        The instantiated interface
    """


    window_utils.clear_screen(window)
    interface = interface_class(window)
    interface.header()
    interface.body()
    interface.footer()
    interface.pack()
    return interface

def launch_application(window):
    """
    Launch the main application interface.
    
    Args:
        window: The tkinter window
        
    Returns:
        The instantiated application interface
    """
    from nationsglory.core.ui import ApplicationInterface
    interface = setup_interface(window, ApplicationInterface)
    return interface

def launch_auto_craft(window):
    """
    Launch the auto craft bot interface.
    
    Args:
        window: The tkinter window
        
    Returns:
        The instantiated auto craft interface
    """
    from nationsglory.core.ui import AutocraftInterface
    print("Launching auto_craft bot")
    interface = setup_interface(window, AutocraftInterface)
    return interface

def launch_server(window):
    """
    Launch the server automation interface.
    
    Args:
        window: The tkinter window
        
    Returns:
        The instantiated server interface
    """
    from nationsglory.core.ui import ServerInterface
    print("Launching server automation bot")
    interface = setup_interface(window, ServerInterface)
    return interface


def main():
    """
    Main entry point for the application.
    """
    try:
        window_utils.focus_window("NationsGlory")
    except Exception as e:
        print(f"Warning: Unable to focus NationsGlory window: {e}")
        print("Please manually switch to the NationsGlory window when needed.")

    window = tk.Tk()
    window.title("NationsGlory Helper")
    window_utils.center_window(window)
    launch_application(window)
    tk.mainloop()


if __name__ == "__main__":
    main()