# /gui/tabs/tab_output.py example as follow # mikro-commander-py/gui/tabs/tab_output.py
"""
Tab for showing command output and logs.
Displays results and logs from command execution.
"""

import tkinter as tk

class OutputTab:
    """
    Tab for output and logs.
    Output is displayed in a read-only text box.
    """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize UI elements for the output tab.
        """
        # Label for the output section
        label = tk.Label(self.frame, text="Command Output & Logs:", font=("Arial", 12))
        label.pack(anchor="w", padx=10, pady=5)

        # Read-only text box for logs and output
        self.textbox = tk.Text(self.frame, height=20, width=80, font=("Consolas", 11), state="disabled")
        self.textbox.pack(padx=10, pady=5, fill="both", expand=True)
        # Future: Add color formatting, filtering, export options, etc.
