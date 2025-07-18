# /gui/app_integration.py example as follow # mikro-commander-py/gui/app_integration.py
"""
Integrates the GUI tabs with the core controller logic.
Handles user actions, validation, and execution workflow.
"""

from core.commander import MikroCommanderController
from core.config import ConfigManager
from core.logger import OutputLogger
from utils.validators import is_valid_ip, is_valid_port, is_non_empty_string

import tkinter as tk
from tkinter import messagebox

class AppIntegration:
    """
    Connects GUI widgets to backend logic; handles 'Execute' action and validation.
    """
    def __init__(
        self,
        commands_tab,
        targets_tab,
        output_tab,
        settings_tab,
        root_window: tk.Tk
    ):
        # Set up logger for output tab
        self.logger = OutputLogger(gui_output_widget=output_tab.textbox)
        # Config manager for persistent settings
        self.config = ConfigManager()
        self.config.load()

        # Core controller for running commands
        self.controller = MikroCommanderController(self.logger, self.config)

        # Store tab references
        self.commands_tab = commands_tab
        self.targets_tab = targets_tab
        self.output_tab = output_tab
        self.settings_tab = settings_tab
        self.root_window = root_window

        # Add Execute button to main window
        self.execute_btn = tk.Button(
            root_window, text="Execute", command=self.execute_commands,
            bg="#28a745", fg="white", font=("Arial", 12, "bold")
        )
        self.execute_btn.pack(pady=10)

    def execute_commands(self):
        """
        Read inputs from GUI, validate, and execute commands on devices.
        Shows messagebox warnings for invalid input.
        """
        # Read commands
        commands = [
            line.strip() for line in self.commands_tab.textbox.get("1.0", tk.END).split("\n")
            if is_non_empty_string(line)
        ]
        if not commands:
            messagebox.showwarning("Validation", "Enter at least one command.")
            return

        # Read targets
        targets = [
            ip.strip() for ip in self.targets_tab.textbox.get("1.0", tk.END).split("\n")
            if is_valid_ip(ip.strip())
        ]
        if not targets:
            messagebox.showwarning("Validation", "Enter at least one valid IP address.")
            return

        # Read settings
        username = self.settings_tab.username_entry.get().strip()
        port = self.settings_tab.port_entry.get().strip()
        threads = self.settings_tab.threads_entry.get().strip()
        host_verification = self.settings_tab.host_verification_var.get()

        if not is_non_empty_string(username):
            messagebox.showwarning("Validation", "Enter SSH username.")
            return
        if not is_valid_port(port):
            messagebox.showwarning("Validation", "Enter a valid SSH port (1-65535).")
            return
        try:
            threads = int(threads)
            if threads < 1:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Validation", "Enter a valid thread count (>0).")
            return

        # Ask for password securely
        password = tk.simpledialog.askstring("Password", f"Enter password for {username}:", show="*")
        if not is_non_empty_string(password):
            messagebox.showwarning("Validation", "Password required.")
            return

        # Save config
        self.config.set("DEFAULT", "username", username)
        self.config.set("DEFAULT", "port", str(port))
        self.config.set("DEFAULT", "threads", str(threads))
        self.config.set("DEFAULT", "verify_host", str(host_verification))
        self.config.save()

        # Clear output area before execution
        self.output_tab.textbox.config(state="normal")
        self.output_tab.textbox.delete("1.0", tk.END)
        self.output_tab.textbox.config(state="disabled")

        # Run commands in background thread to avoid blocking UI
        import threading
        threading.Thread(
            target=lambda: self.controller.execute_on_targets(
                commands, targets, username, password, int(port), threads, host_verification
            ),
            daemon=True
        ).start()
