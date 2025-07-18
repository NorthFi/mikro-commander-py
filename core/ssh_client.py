# /core/ssh_client.py example as follow # mikro-commander-py/core/ssh_client.py
"""
Handles SSH connections and command execution to MikroTik devices.
Uses Paramiko for SSH protocol.
"""

import paramiko
from typing import Optional

class SSHClient:
    """
    SSH client wrapper for connecting and executing commands on MikroTik devices.
    """
    def __init__(self, ip: str, username: str, password: str, port: int, host_verification: bool, logger):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.host_verification = host_verification
        self.logger = logger
        self.client: Optional[paramiko.SSHClient] = None

    def connect(self) -> bool:
        """
        Establish SSH connection.
        Returns True if successful, False otherwise.
        """
        try:
            self.client = paramiko.SSHClient()
            if self.host_verification:
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(paramiko.RejectPolicy())
            else:
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.ip,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=10
            )
            self.logger.log_info(f"{self.ip}: Connected.")
            return True
        except paramiko.AuthenticationException:
            self.logger.log_error(f"{self.ip}: Authentication failed.")
        except paramiko.SSHException as e:
            self.logger.log_error(f"{self.ip}: SSH error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"{self.ip}: Connection error: {str(e)}")
        return False

    def execute(self, command: str) -> str:
        """
        Execute a command via SSH.
        Returns output string or error.
        """
        if not self.client:
            return "Not connected"
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                return f"Error: {error.strip()}"
            return output.strip() if output else "Success"
        except Exception as e:
            return f"Command error: {str(e)}"

    def disconnect(self):
        """
        Close SSH connection.
        """
        if self.client:
            self.client.close()
            self.logger.log_info(f"{self.ip}: Disconnected.")
