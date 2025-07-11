# In nationsglory/utils/window_utils.py

import platform
import subprocess
import tkinter as tk

def focus_window(window_name):
    """
    Focus a window by name, with cross-platform support.

    Args:
        window_name: Name of the window to focus

    Returns:
        True if successful, False otherwise
    """
    system = platform.system()

    if system == "Windows":
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(window_name)
            if windows:
                windows[0].activate()
                return True
        except ImportError:
            print("PyGetWindow not available, cannot focus window on Windows")
        except Exception as e:
            print(f"Error focusing window on Windows: {e}")

    elif system == "Darwin":  # macOS
        try:
            cmd = f"""
            osascript -e 'tell application "System Events"
                set frontmost of every process whose name contains "{window_name}" to true
            end tell'
            """
            subprocess.run(cmd, shell=True)
            return True
        except Exception as e:
            print(f"Error focusing window on macOS: {e}")

    elif system == "Linux":
        try:
            # Try using xdotool if available
            try:
                # Check if xdotool is installed
                subprocess.run(["which", "xdotool"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Use xdotool to focus window
                cmd = f"xdotool search --name '{window_name}' windowactivate"
                subprocess.run(cmd, shell=True)
                return True
            except subprocess.CalledProcessError:
                # If xdotool is not available, try wmctrl
                try:
                    subprocess.run(["which", "wmctrl"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    cmd = f"wmctrl -a '{window_name}'"
                    subprocess.run(cmd, shell=True)
                    return True
                except subprocess.CalledProcessError:
                    print("Neither xdotool nor wmctrl is available on this Linux system")
                    print("Install with: sudo apt-get install xdotool or sudo apt-get install wmctrl")
        except Exception as e:
            print(f"Error focusing window on Linux: {e}")

    print(f"Could not focus window '{window_name}' on {system}. Continuing without focus.")
    return False

def clear_screen(window):
    """
    Clear all widgets from a tkinter window.

    Args:
        window: The tkinter window to clear
    """
    for widget in window.winfo_children():
        widget.destroy()

def center_window(window, width=800, height=600):
    """
    Center a tkinter window on the screen.

    Args:
        window: The tkinter window to center
        width: The width of the window
        height: The height of the window
    """
    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))