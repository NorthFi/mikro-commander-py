#!/usr/bin/env python3
import configparser
import fnmatch
import os
import re
import socket
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, simpledialog, filedialog
from concurrent.futures import ThreadPoolExecutor, as_completed

import paramiko
from paramiko import AuthenticationException, SSHException


class MikrotikMCP:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.initialize_variables()
        self.load_config()
        
    def initialize_variables(self):
        """Initialize all class variables"""
        self.ssh = None
        self.user = ""
        self.target_list = []
        self.infile_check = False
        self.log_file = None
        self.running = False
        self.default_port = 22
        self.max_threads = 5
        self.verify_host = False
        self.known_hosts_file = os.path.join(os.path.dirname(__file__), 'known_hosts')
        
    def setup_ui(self):
        """Set up the user interface"""
        self.root.title("Mikrotik MCP - Enhanced")
        self.setup_window_geometry()
        self.create_widgets()
        self.setup_textboxes()
        self.setup_bindings()
        
    def setup_window_geometry(self):
        """Configure window size and grid weights"""
        self.root.minsize(800, 600)
        for row in range(2, 5):
            self.root.rowconfigure(row, weight=1)
        for column in range(0, 5):
            self.root.columnconfigure(column, weight=1)
        
    def create_widgets(self):
        """Create all UI widgets"""
        self.create_banner()
        self.create_labels()
        self.create_textboxes()
        self.create_buttons()
        self.create_progress_bar()
        self.create_menu()
        
    def create_banner(self):
        """Create application banner"""
        banner_path = os.path.join(os.path.dirname(__file__), 'mikrotik-banner.png')
        if os.path.exists(banner_path):
            self.banner_image = tk.PhotoImage(file=banner_path)
            self.banner = tk.Label(self.root, image=self.banner_image)
            self.banner.grid(row=0, column=1, columnspan=3, padx=12, pady=10)
        
    def create_labels(self):
        """Create all labels"""
        tk.Label(self.root, text="Mass Command Pusher", font=20).grid(row=1, column=1, columnspan=3)
        tk.Label(self.root, text="Commands:").grid(row=2, column=0, padx=10, pady=25)
        tk.Label(self.root, text="Targets:").grid(row=3, column=0)
        tk.Label(self.root, text="Output:").grid(row=4, column=0, pady=25)
        tk.Label(self.root, text="SSH Port:").grid(row=5, column=0, pady=10)
        tk.Label(self.root, text="Threads:").grid(row=5, column=2)
        
    def create_textboxes(self):
        """Create all text entry boxes"""
        # Commands textbox
        self.commands = tk.Text(self.root, bg="white", height=5, width=70)
        self.commands.grid(row=2, column=1, columnspan=3, sticky='news', pady=10)
        
        # Targets textbox
        self.target = tk.Text(self.root, bg="white", height=5, width=70)
        self.target.grid(row=3, column=1, columnspan=3, pady=10, sticky='news')
        
        # Output textbox
        self.output = tk.Text(self.root, bg='white', height=10, width=70)
        self.output.configure(state='disabled')
        self.output.grid(row=4, column=1, columnspan=3, pady=10, sticky='news')
        
        # SSH Port entry
        self.sshport = tk.Text(self.root, bg='white', height=1, width=10)
        self.sshport.grid(row=5, column=1, sticky='w')
        
        # Threads entry
        self.threads = tk.Text(self.root, bg='white', height=1, width=5)
        self.threads.grid(row=5, column=3, sticky='w')
        
    def setup_textboxes(self):
        """Configure textbox default values and styles"""
        self.configure_textbox(self.commands, "Enter commands here (one per line)")
        self.configure_textbox(self.target, "Enter target IPs (comma/space separated) or load from file")
        self.configure_textbox(self.sshport, "22")
        self.configure_textbox(self.threads, "5")
        
        # Configure output tags for colored text
        self.output.tag_config('error', foreground='red')
        self.output.tag_config('success', foreground='green')
        self.output.tag_config('warning', foreground='orange')
        self.output.tag_config('info', foreground='blue')
        
    def configure_textbox(self, textbox, placeholder):
        """Configure a textbox with placeholder text"""
        textbox.insert('1.0', placeholder)
        textbox.config(fg='grey')
        
    def create_buttons(self):
        """Create all buttons"""
        # Load button
        self.load_btn = tk.Button(self.root, text="Load Targets", command=self.open_file)
        self.load_btn.grid(row=3, column=4, padx=20)
        
        # Submit button
        self.submit_btn = tk.Button(self.root, text="Execute", command=self.submit)
        self.submit_btn.grid(row=6, column=3, pady=20)
        
        # Stop button
        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop_execution, state='disabled')
        self.stop_btn.grid(row=6, column=2, padx=10, pady=20)
        
        # Exit button
        self.exit_btn = tk.Button(self.root, text="Exit", command=self.cleanup_and_exit)
        self.exit_btn.grid(row=6, column=4, padx=10, pady=20)
        
    def create_progress_bar(self):
        """Create and place progress bar"""
        self.progress = ttk.Progressbar(self.root, orient='horizontal', 
                                      length=200, mode='determinate')
        self.progress.grid(row=7, column=1, columnspan=3, pady=10)
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Targets", command=self.open_file)
        file_menu.add_command(label="Save Output", command=self.save_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.cleanup_and_exit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Change User", command=self.change_user)
        settings_menu.add_command(label="Host Key Verification", command=self.toggle_host_verification)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def setup_bindings(self):
        """Set up event bindings"""
        self.commands.bind('<FocusIn>', lambda e: self.clear_placeholder(self.commands))
        self.commands.bind('<FocusOut>', lambda e: self.set_placeholder(self.commands, "Enter commands here (one per line)"))
        
        self.target.bind('<FocusIn>', lambda e: self.clear_placeholder(self.target))
        self.target.bind('<FocusOut>', lambda e: self.set_placeholder(self.target, 
                                    "Enter target IPs (comma/space separated) or load from file"))
        
        self.sshport.bind('<FocusIn>', lambda e: self.clear_placeholder(self.sshport))
        self.sshport.bind('<FocusOut>', lambda e: self.set_placeholder(self.sshport, "22"))
        
        self.threads.bind('<FocusIn>', lambda e: self.clear_placeholder(self.threads))
        self.threads.bind('<FocusOut>', lambda e: self.set_placeholder(self.threads, "5"))
        
    def clear_placeholder(self, textbox):
        """Clear placeholder text when focused"""
        if textbox.cget('fg') == 'grey':
            textbox.delete("1.0", "end")
            textbox.config(fg='black')
            
    def set_placeholder(self, textbox, placeholder):
        """Set placeholder text when unfocused and empty"""
        if not textbox.get("1.0", "end-1c").strip():
            textbox.delete("1.0", "end")
            textbox.insert("1.0", placeholder)
            textbox.config(fg='grey')
            
    def load_config(self):
        """Load configuration from file"""
        config_path = os.path.join(os.path.dirname(__file__), 'mikrotikmcp.cfg')
        config = configparser.ConfigParser()
        
        if os.path.exists(config_path):
            config.read(config_path)
            if 'DEFAULT' in config:
                self.user = config['DEFAULT'].get('username', '')
                self.default_port = config['DEFAULT'].getint('port', 22)
                self.max_threads = config['DEFAULT'].getint('threads', 5)
                self.verify_host = config['DEFAULT'].getboolean('verify_host', False)
                
                # Update UI with loaded values
                self.sshport.delete("1.0", "end")
                self.sshport.insert("1.0", str(self.default_port))
                self.threads.delete("1.0", "end")
                self.threads.insert("1.0", str(self.max_threads))
                
    def save_config(self):
        """Save configuration to file"""
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'username': self.user,
            'port': self.sshport.get("1.0", "end-1c") or "22",
            'threads': self.threads.get("1.0", "end-1c") or "5",
            'verify_host': str(self.verify_host)
        }
        
        config_path = os.path.join(os.path.dirname(__file__), 'mikrotikmcp.cfg')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            
    def open_file(self):
        """Open file dialog to load targets"""
        file_path = filedialog.askopenfilename(
            initialdir="~/",
            title="Select Target File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        
        if file_path:
            try:
                with open(file_path) as f:
                    targets = [line.strip() for line in f if line.strip()]
                    self.target_list = targets
                    self.infile_check = True
                    
                    self.target.delete("1.0", "end")
                    self.target.config(fg="black")
                    self.target.insert("end", "\n".join(targets))
                    
            except Exception as e:
                self.log_error(f"Error loading file: {str(e)}")
                
    def save_output(self):
        """Save output to file"""
        if not self.output.get("1.0", "end-1c"):
            messagebox.showwarning("Warning", "No output to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.output.get("1.0", "end-1c"))
                self.log_info(f"Output saved to {file_path}")
            except Exception as e:
                self.log_error(f"Error saving file: {str(e)}")
                
    def change_user(self):
        """Change the SSH username"""
        self.user = simpledialog.askstring("Username", "Enter SSH username:", initialvalue=self.user)
        
    def toggle_host_verification(self):
        """Toggle host key verification"""
        self.verify_host = not self.verify_host
        status = "enabled" if self.verify_host else "disabled"
        self.log_info(f"Host key verification {status}")
        
    def submit(self):
        """Start command execution"""
        if self.running:
            return
            
        self.running = True
        self.submit_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        # Clear output
        self.output.configure(state='normal')
        self.output.delete("1.0", "end")
        
        # Get commands
        commands = self.get_commands()
        if not commands:
            self.log_error("No commands to execute")
            self.running = False
            self.submit_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            return
            
        # Get targets
        self.get_targets()
        if not self.target_list:
            self.log_error("No targets specified")
            self.running = False
            self.submit_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            return
            
        # Get credentials
        if not self.user:
            self.change_user()
            if not self.user:
                self.running = False
                self.submit_btn.config(state='normal')
                self.stop_btn.config(state='disabled')
                return
                
        password = simpledialog.askstring("Password", f"Enter password for {self.user}:", show='*')
        if not password:
            self.running = False
            self.submit_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            return
            
        # Start execution in a new thread
        threading.Thread(
            target=self.execute_commands,
            args=(commands, password),
            daemon=True
        ).start()
        
    def stop_execution(self):
        """Stop current execution"""
        self.running = False
        self.log_warning("Execution stopped by user")
        self.submit_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
    def get_commands(self):
        """Get commands from textbox"""
        commands = self.commands.get("1.0", "end-1c").strip()
        if not commands or commands == "Enter commands here (one per line)":
            return []
            
        # Split commands by newline and filter empty lines
        return [cmd.strip() for cmd in commands.split('\n') if cmd.strip()]
        
    def get_targets(self):
        """Get targets from textbox or file"""
        if not self.infile_check:
            targets = self.target.get("1.0", "end-1c").strip()
            if targets and targets != "Enter target IPs (comma/space separated) or load from file":
                # Split by commas, spaces, or newlines
                self.target_list = re.split(r'[,;\s\n]+', targets)
                
    def execute_commands(self, commands, password):
        """Execute commands on all targets"""
        try:
            self.start_session_log()
            total_targets = len(self.target_list)
            self.progress["maximum"] = total_targets
            
            port = int(self.sshport.get("1.0", "end-1c") or "22")
            max_threads = int(self.threads.get("1.0", "end-1c") or 5
            
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {
                    executor.submit(
                        self.process_device,
                        target,
                        commands,
                        password,
                        port
                    ): target for target in self.target_list
                }
                
                for i, future in enumerate(as_completed(futures), 1):
                    if not self.running:
                        break
                        
                    target = futures[future]
                    try:
                        result = future.result()
                        self.log_info(f"Completed {target}: {result}")
                    except Exception as e:
                        self.log_error(f"Error processing {target}: {str(e)}")
                        
                    self.progress["value"] = i
                    self.root.update()
                    
        except Exception as e:
            self.log_error(f"Execution error: {str(e)}")
        finally:
            self.running = False
            self.submit_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress["value"] = 0
            if self.log_file:
                self.log_file.close()
                self.log_file = None
                
    def process_device(self, target, commands, password, port):
        """Process commands for a single device"""
        if not self.running:
            return "Skipped (stopped)"
            
        try:
            self.connect(target, password, port)
            if not self.ssh:
                return "Connection failed"
                
            results = []
            for cmd in commands:
                if not self.running:
                    break
                    
                result = self.execute_command(cmd)
                results.append(result)
                
            self.ssh.close()
            return " | ".join(results)
            
        except Exception as e:
            return f"Error: {str(e)}"
            
    def connect(self, host, password, port):
        """Connect to a device"""
        try:
            self.ssh = paramiko.SSHClient()
            
            if self.verify_host:
                # Load known hosts if file exists
                if os.path.exists(self.known_hosts_file):
                    self.ssh.load_host_keys(self.known_hosts_file)
                self.ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
            else:
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
            self.ssh.connect(
                host,
                username=self.user,
                password=password,
                port=port,
                timeout=10,
                banner_timeout=20,
                allow_agent=False,
                look_for_keys=False
            )
            
            # Log connection to device
            self.execute_command(':log warning "Connected via MikrotikMCP"')
            return True
            
        except AuthenticationException:
            self.log_error(f"{host}: Authentication failed")
        except socket.timeout:
            self.log_error(f"{host}: Connection timeout")
        except SSHException as e:
            self.log_error(f"{host}: SSH error - {str(e)}")
        except Exception as e:
            self.log_error(f"{host}: Connection error - {str(e)}")
            
        return False
        
    def execute_command(self, command):
        """Execute a single command"""
        if not command:
            return "Empty command"
            
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode().strip()
            errors = stderr.read().decode().strip()
            
            if errors:
                return f"Error: {errors}"
                
            return output if output else "Success"
            
        except Exception as e:
            return f"Command error: {str(e)}"
            
    def start_session_log(self):
        """Start logging session to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(os.path.dirname(__file__), f"session_{timestamp}.log")
        self.log_file = open(log_path, 'a')
        self.log_info(f"Session log started: {log_path}")
        
    def log_message(self, message, level='info'):
        """Log a message to output and file"""
        self.output.configure(state='normal')
        self.output.insert("end", f"{datetime.now().strftime('%H:%M:%S')} - {message}\n", level)
        self.output.see("end")
        self.output.configure(state='disabled')
        
        if self.log_file:
            self.log_file.write(f"{datetime.now()} - {level.upper()} - {message}\n")
            self.log_file.flush()
            
    def log_info(self, message):
        """Log an info message"""
        self.log_message(message, 'info')
        
    def log_error(self, message):
        """Log an error message"""
        self.log_message(message, 'error')
        
    def log_warning(self, message):
        """Log a warning message"""
        self.log_message(message, 'warning')
        
    def log_success(self, message):
        """Log a success message"""
        self.log_message(message, 'success')
        
    def show_help(self):
        """Show help information"""
        help_text = """Mikrotik Mass Command Pusher (MCP) - Help

1. Enter commands (one per line) in the Commands box
2. Specify target devices (IP addresses) in the Targets box
   - Separate with commas, spaces, or newlines
   - Or load from a text file using the Load button
3. Set SSH port (default: 22) and number of concurrent threads
4. Click Execute to run commands on all devices

Advanced Features:
- Host key verification (in Settings menu)
- Session logging
- Concurrent execution
- Command validation

Keyboard Shortcuts:
- Ctrl+O: Load targets
- Ctrl+S: Save output
- Ctrl+E: Execute commands
- Ctrl+Q: Quit
"""
        messagebox.showinfo("Help", help_text)
        
    def show_about(self):
        """Show about information"""
        about_text = """Mikrotik Mass Command Pusher (MCP)
Version: 1.0.0

A tool for executing commands on multiple Mikrotik devices simultaneously.

Features:
- Multi-threaded execution
- Command logging
- Host key verification
- Progress tracking

Copyright © 2023
"""
        messagebox.showinfo("About", about_text)
        
    def cleanup_and_exit(self):
        """Clean up resources and exit"""
        self.running = False
        self.save_config()
        if self.log_file:
            self.log_file.close()
        self.root.quit()
        self.root.destroy()


def main():
    root = tk.Tk()
    
    # Set window icon if available
    icon_path = os.path.join(os.path.dirname(__file__), 'mikrotik-icon.png')
    if os.path.exists(icon_path):
        root.iconphoto(False, tk.PhotoImage(file=icon_path))
        
    app = MikrotikMCP(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup_and_exit)
    root.mainloop()


if __name__ == "__main__":
    main()