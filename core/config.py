# /core/config.py example as follow # mikro-commander-py/core/config.py
"""
Handles reading and writing application configuration.
Supports settings for SSH, threads, and host verification.
"""

import configparser
from typing import Optional

class ConfigManager:
    """
    Manages application configuration using configparser.
    """
    def __init__(self, config_path: str = "mikrocommander.cfg"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

    def load(self):
        """
        Load configuration from config file.
        """
        self.config.read(self.config_path)

    def get(self, section: str, option: str, fallback: Optional[str] = None):
        """
        Get a configuration value with optional fallback.
        """
        return self.config.get(section, option, fallback=fallback)

    def set(self, section: str, option: str, value: str):
        """
        Set a configuration value.
        """
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, option, value)

    def save(self):
        """
        Save configuration to file.
        """
        with open(self.config_path, "w") as f:
            self.config.write(f)

    def get_all_settings(self) -> dict:
        """
        Return all settings as a dictionary.
        """
        return {section: dict(self.config.items(section)) for section in self.config.sections()}
