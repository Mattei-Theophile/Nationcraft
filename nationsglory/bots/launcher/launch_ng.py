import os
import platform
import subprocess
import time
import logging
from typing import Optional, Dict, Any
import json


class NationsGloryLauncher:
    """
    Class for automatically launching NationsGlory and Minecraft on different platforms.
    """

    def __init__(self, config_path: Optional[str] = "nationsglory/config/launcher_config.json"):
        """
        Initialize the launcher with platform-specific settings.

        Args:
            config_path: Optional path to a config file with launcher settings
        """

        self.platform = platform.system()
        self.logger = self._setup_logger()
        self.config = self._load_config(config_path)


        # Override with config if available
        if self.config and 'executable_path' in self.config:
            self.executable_path = self.config['executable_path']

        self.logger.info(f"Initialized launcher for {self.platform}")
        self.logger.info(f"Using executable path: {self.executable_path}")

    def _setup_logger(self) -> logging.Logger:
        """Set up and configure logging."""
        logger = logging.getLogger('NationsGloryLauncher')
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def _load_config(self, config_path: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Load configuration from a JSON file if provided.

        Args:
            config_path: Path to the config file

        Returns:
            Dictionary with configuration or None if no config path provided
        """
        if not config_path:
            return None

        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load config: {e}")
            return None

    def _get_default_path(self) -> str:
        """
        Get the default path for NationsGlory launcher based on the platform.

        Returns:
            The path to the NationsGlory executable
        """
        if self.platform == "Windows":
            # Common Windows installation paths
            paths_to_check = [
                os.path.join(os.environ.get('APPDATA', ''), 'NationsGlory', 'NationsGlory.exe'),
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'NationsGlory', 'NationsGlory.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'NationsGlory', 'NationsGlory.exe')
            ]

            for path in paths_to_check:
                if os.path.exists(path):
                    return path

            # Default to AppData location if not found
            return os.path.join(os.environ.get('APPDATA', ''), 'NationsGlory', 'NationsGlory.exe')

        elif self.platform == "Linux":
            # Common Linux installation paths
            paths_to_check = [
                os.path.expanduser('~//squashfs-root/nationsglory'),
                '/opt/nationsglory/nationsglory',
                os.path.expanduser('~/NationsGlory/nationsglory')
            ]

            for path in paths_to_check:
                if os.path.exists(path):
                    return path

            # Default to user home location if not found
            return os.path.expanduser('~/.nationsglory/nationsglory')

        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            raise NotImplementedError(f"Platform {self.platform} is not supported")

    def validate_installation(self) -> bool:
        """
        Check if the NationsGlory launcher is installed at the expected location.

        Returns:
            True if the launcher exists, False otherwise
        """
        if not os.path.exists(self.executable_path):
            self.logger.error(f"NationsGlory launcher not found at {self.executable_path}")
            return False

        self.logger.info(f"NationsGlory launcher found at {self.executable_path}")
        return True

    def launch_nationsglory(self) -> bool:
        """
        Launch the NationsGlory launcher application.

        Returns:
            True if launched successfully, False otherwise
        """
        if not self.validate_installation():
            return False

        try:
            self.logger.info("Launching NationsGlory...")

            if self.platform == "Windows":
                subprocess.Popen([self.executable_path])
            elif self.platform == "Linux":
                subprocess.Popen([self.executable_path], shell=True)

            self.logger.info("NationsGlory launcher started")
            return True

        except Exception as e:
            self.logger.error(f"Failed to launch NationsGlory: {e}")
            return False

    def launch_minecraft(self, auto_login: bool = False, server: Optional[str] = None,
                         wait_time: int = 10) -> bool:
        """
        Launch NationsGlory and start Minecraft.

        Args:
            auto_login: Whether to attempt auto-login
            server: Optional server to connect to
            wait_time: Time to wait for launcher to initialize before launching Minecraft

        Returns:
            True if launched successfully, False otherwise
        """
        if not self.launch_nationsglory():
            return False

        self.logger.info(f"Waiting {wait_time} seconds for launcher to initialize...")
        time.sleep(wait_time)

        try:
            self.logger.info("Attempting to start Minecraft...")

            # Platform-specific implementations for launching Minecraft from NationsGlory
            if self.platform == "Windows":
                # On Windows, we can try to find and click the Play button using automation
                # This is a simplified approach, as we don't have PyAutoGUI
                minecraft_process = None

                # Check if configuration provides any way to directly launch Minecraft
                if self.config and 'minecraft_command' in self.config:
                    minecraft_command = self.config['minecraft_command']
                    minecraft_process = subprocess.Popen(minecraft_command, shell=True)
                else:
                    self.logger.warning("No direct Minecraft command found in config")
                    self.logger.info("Waiting for user to manually click Play...")

            elif self.platform == "Linux":
                # On Linux, we can try to find the Minecraft process or executable
                # This is a simplified approach
                minecraft_process = None

                # Check if configuration provides any way to directly launch Minecraft
                if self.config and 'minecraft_command' in self.config:
                    minecraft_command = self.config['minecraft_command']
                    minecraft_process = subprocess.Popen(minecraft_command, shell=True)
                else:
                    self.logger.warning("No direct Minecraft command found in config")
                    self.logger.info("Waiting for user to manually click Play...")

            # If auto_login is enabled, we would handle that here
            if auto_login:
                self.logger.info("Auto-login requested, but not implemented yet")
                # Implementation would depend on how NationsGlory handles authentication

            # If server connection is requested, we would handle that here
            if server:
                self.logger.info(f"Server connection to {server} requested, but not implemented yet")
                # Implementation would depend on how servers are joined

            self.logger.info("Minecraft launch initiated")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start Minecraft: {e}")
            return False

