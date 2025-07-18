"""
SettingsTab with Export/Import config buttons.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from utils.config_io import export_config, import_config

class SettingsTab:
    # ... existing __init__ ...
    def add_export_import_buttons(self, config_manager):
        self.export_btn = tk.Button(self.frame, text="Export Config", command=lambda: self.export_config_action(config_manager))
        self.export_btn.pack(side="left", padx=8, pady=8)
        self.import_btn = tk.Button(self.frame, text="Import Config", command=lambda: self.import_config_action(config_manager))
        self.import_btn.pack(side="left", padx=8, pady=8)

    def export_config_action(self, config_manager):
        path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI Files", "*.ini")])
        if path:
            try:
                export_config(config_manager, path)
                messagebox.showinfo("Export Config", f"Configuration exported to {path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def import_config_action(self, config_manager):
        path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
        if path:
            try:
                import_config(config_manager, path)
                messagebox.showinfo("Import Config", f"Configuration imported from {path}")
            except Exception as e:
                messagebox.showerror("Import Error", str(e))
