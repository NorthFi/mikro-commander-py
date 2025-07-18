# /main.py example as follow # mikro-commander-py/main.py
"""
Main entry point for Mikro Commander application.
Integrates GUI tabs and core logic, sets up the main window, and wires user actions to backend execution.
Adds SettingsTab with config export/import.
"""

import tkinter as tk
from gui.main import MikroCommanderApp
from gui.app_integration import AppIntegration
from core.config import ConfigManager

def main():
    """
    Initialize main Tkinter window, set up the tabbed GUI,
    and connect GUI events to application logic.
    Includes export/import config functionality in SettingsTab.
    """
    # Create main window
    root = tk.Tk()
    # Initialize main GUI with tabs
    app = MikroCommanderApp(root)
    
    # Create configuration manager (pass path as needed)
    config_manager = ConfigManager()

    # Wire up the tabs to backend logic via AppIntegration
    integration = AppIntegration(
        commands_tab=app.commands_tab,
        targets_tab=app.targets_tab,
        output_tab=app.output_tab,
        settings_tab=app.settings_tab,
        root_window=root,
        config=config_manager
    )

    # Add Export/Import config buttons to Settings tab
    app.settings_tab.add_export_import_buttons(config_manager)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
