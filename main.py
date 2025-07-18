# /main.py example as follow # mikro-commander-py/main.py
"""
Main entry point for Mikro Commander GUI.
Initializes the tkinter root and launches the tabbed GUI.
"""

import tkinter as tk
from gui.main import MikroCommanderApp  # Main GUI application class

def main():
    """
    Create main Tkinter window and launch the GUI application.
    """
    root = tk.Tk()
    app = MikroCommanderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
