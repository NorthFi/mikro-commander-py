# /main.py example as follow # mikro-commander-py/main.py
"""
Main entry point for Mikro Commander application.
Integrates GUI tabs and core logic, sets up the main window, and wires user actions to backend execution.
"""

import tkinter as tk
from gui.main import MikroCommanderApp
from gui.app_integration import AppIntegration

def main():
    """
    Initialize main Tkinter window, set up the tabbed GUI,
    and connect GUI events to application logic.
    """
    # Create main window
    root = tk.Tk()
    # Initialize main GUI with tabs
    app = MikroCommanderApp(root)
    
    # Wire up the tabs to backend logic via AppIntegration
    # Access tab objects from the GUI app
    # These are public attributes as set up in gui/main.py
    integration = AppIntegration(
        commands_tab=app.commands_tab,
        targets_tab=app.targets_tab,
        output_tab=app.output_tab,
        settings_tab=app.settings_tab,
        root_window=root
    )
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
