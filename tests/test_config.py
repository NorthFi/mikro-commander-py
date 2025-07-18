# /tests/test_config.py example as follow # mikro-commander-py/tests/test_config.py
"""
Unit tests for ConfigManager in core/config.py.
"""

import tempfile
import os
from core.config import ConfigManager

def test_config_save_and_load():
    # Create a temp file for config
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        config_path = tmp.name
    manager = ConfigManager(config_path)
    manager.set("DEFAULT", "username", "testuser")
    manager.save()
    manager2 = ConfigManager(config_path)
    manager2.load()
    assert manager2.get("DEFAULT", "username") == "testuser"
    os.remove(config_path)

def test_get_all_settings():
    manager = ConfigManager()
    manager.set("SECTION", "key", "value")
    manager.save()
    manager.load()
    settings = manager.get_all_settings()
    assert "SECTION" in settings
    assert settings["SECTION"]["key"] == "value"
