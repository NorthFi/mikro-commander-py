"""
Helpers for exporting and importing Mikro Commander configuration files.
"""

import configparser
import os

def export_config(config_manager, export_path):
    """
    Export current config to export_path (.ini format).
    """
    with open(export_path, "w") as f:
        config_manager.config.write(f)

def import_config(config_manager, import_path):
    """
    Import config from import_path (.ini format).
    Overwrites current config in memory and saves.
    """
    if not os.path.exists(import_path):
        raise FileNotFoundError(f"Config file '{import_path}' not found.")
    config_manager.config.read(import_path)
    config_manager.save()
