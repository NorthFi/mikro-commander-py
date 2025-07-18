# /gui/tabs/tab_commands.py example as follow # mikro-commander-py/gui/tabs/tab_commands.py
"""
Tab for entering RouterOS commands.
Allows users to input commands to be run on MikroTik devices.
"""

import tkinter as tk

class CommandsTab:
    """
    Tab for RouterOS command input.
    Provides a large text box for multi-line commands.
    """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize UI elements for the commands tab.
        """
        # Label for the command text box
        label = tk.Label(self.frame, text="Enter RouterOS Commands (one per line):", font=("Arial", 12))
        label.pack(anchor="w", padx=10, pady=5)

        # Multi-line text box for commands
        self.textbox = tk.Text(self.frame, height=15, width=80, font=("Consolas", 11))
        self.textbox.pack(padx=10, pady=5, fill="both", expand=True)
        # Future: Add syntax highlighting, command validation, etc.
