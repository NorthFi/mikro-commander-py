# /gui/tabs/tab_targets.py example as follow # mikro-commander-py/gui/tabs/tab_targets.py
"""
Tab for entering and loading target device IPs.
Allows manual entry and loading from a text file.
"""

import tkinter as tk
from tkinter import filedialog

class TargetsTab:
    """
    Tab for specifying target IP addresses.
    Supports manual entry and file-based loading.
    """
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.setup_ui()

    def setup_ui(self):
        """
        Initialize UI elements for the targets tab.
        """
        # Label for the targets text box
        label = tk.Label(self.frame, text="Target Device IP Addresses:", font=("Arial", 12))
        label.pack(anchor="w", padx=10, pady=5)

        # Multi-line text box for IP addresses
        self.textbox = tk.Text(self.frame, height=10, width=80, font=("Consolas", 11))
        self.textbox.pack(padx=10, pady=5, fill="both", expand=True)

        # Button to load IPs from a file
        load_button = tk.Button(self.frame, text="Load from File", command=self.load_targets)
        load_button.pack(pady=5)

    def load_targets(self):
        """
        Open a file dialog to select a text file and load its contents into the textbox.
        Each line is assumed to be an IP address.
        """
        file_path = filedialog.askopenfilename(
            title="Select Target File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as f:
                ips = f.read()
                self.textbox.delete("1.0", tk.END)
                self.textbox.insert(tk.END, ips)
        # Future: Add IP address validation, duplicate removal, etc.
