# /gui/tabs/tab_settings.py example as follow # mikro-commander-py/gui/tabs/tab_settings.py
"""
Tab for user settings, SSH, threads, etc.
Allows configuration of connection and execution parameters.
"""

import tkinter as tk

class SettingsTab:
    """
    Tab for application settings.
    Includes SSH username, port, thread count, and host verification toggle.
    """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize UI elements for the settings tab.
        """
        # Label for the settings section
        label = tk.Label(self.frame, text="Settings:", font=("Arial", 12))
        label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # SSH username entry
        tk.Label(self.frame, text="SSH Username:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        # SSH port entry
        tk.Label(self.frame, text="SSH Port:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.port_entry = tk.Entry(self.frame, width=10)
        self.port_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Max threads entry
        tk.Label(self.frame, text="Max Threads:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.threads_entry = tk.Entry(self.frame, width=10)
        self.threads_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Host key verification checkbox
        self.host_verification_var = tk.BooleanVar()
        host_verification_checkbox = tk.Checkbutton(
            self.frame,
            text="Enable SSH Host Key Verification",
            variable=self.host_verification_var
        )
        host_verification_checkbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        # Future: Add config save/load, advanced options, etc.
