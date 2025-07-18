# /core/logger.py example as follow # mikro-commander-py/core/logger.py
"""
Handles logging and output to GUI and log files.
Supports color coding and log levels.
"""

from typing import Optional

class OutputLogger:
    """
    Logger for GUI output and optional log file.
    Can be extended to support colors, filtering, and external logging.
    """
    def __init__(self, gui_output_widget: Optional[object] = None, logfile_path: Optional[str] = None):
        self.output_widget = gui_output_widget  # Typically a tk.Text widget
        self.logfile_path = logfile_path
        self.logfile = None
        if logfile_path:
            self.logfile = open(logfile_path, "a")

    def log_info(self, message: str):
        """
        Log informational message.
        """
        self._write(message, "INFO")

    def log_error(self, message: str):
        """
        Log error message.
        """
        self._write(message, "ERROR")

    def log_success(self, message: str):
        """
        Log success message.
        """
        self._write(message, "SUCCESS")

    def _write(self, message: str, level: str):
        """
        Write message to GUI and/or log file.
        """
        formatted = f"[{level}] {message}\n"
        # Write to GUI output widget if available
        if self.output_widget:
            self.output_widget.config(state="normal")
            self.output_widget.insert("end", formatted)
            self.output_widget.see("end")
            self.output_widget.config(state="disabled")
        # Write to file if enabled
        if self.logfile:
            self.logfile.write(formatted)
            self.logfile.flush()

    def close(self):
        """
        Close log file if open.
        """
        if self.logfile:
            self.logfile.close()
