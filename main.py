"""
Main entry point for Mikro Commander GUI.
"""

import sys
import os
import tkinter as tk
from gui.main import MikroCommanderApp

def main():
    root = tk.Tk()
    app = MikroCommanderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
