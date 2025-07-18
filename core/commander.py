# /core/commander.py example as follow # mikro-commander-py/core/commander.py
"""
Main controller class for command execution and coordination.
Handles orchestration between GUI, SSH, config, and logging modules.
"""

from core.ssh_client import SSHClient
from core.config import ConfigManager
from core.logger import OutputLogger
from typing import List, Optional

class MikroCommanderController:
    """
    Coordinates execution of commands on multiple devices using SSH.
    Manages configuration, logging, and execution threads.
    """
    def __init__(self, logger: OutputLogger, config: ConfigManager):
        # Output logger for displaying results and errors
        self.logger = logger
        # Configuration manager for settings and credentials
        self.config = config

    def execute_on_targets(self, commands: List[str], targets: List[str], username: str, password: str, port: int, threads: int, host_verification: bool):
        """
        Execute a list of commands on all target devices.

        Args:
            commands: List of RouterOS commands to execute.
            targets: List of IP addresses.
            username: SSH user.
            password: SSH password.
            port: SSH port number.
            threads: Number of concurrent threads.
            host_verification: Whether to verify SSH host keys.
        """
        import concurrent.futures

        self.logger.log_info(f"Starting execution on {len(targets)} targets...")

        def run_on_target(ip: str) -> str:
            ssh = SSHClient(ip, username, password, port, host_verification, self.logger)
            result_lines = []
            if not ssh.connect():
                return f"{ip}: Connection failed"
            for cmd in commands:
                output = ssh.execute(cmd)
                result_lines.append(f"{cmd}: {output}")
            ssh.disconnect()
            return f"{ip}:\n" + "\n".join(result_lines)

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_ip = {executor.submit(run_on_target, ip): ip for ip in targets}
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    self.logger.log_info(result)
                    results.append(result)
                except Exception as e:
                    self.logger.log_error(f"{ip}: Execution error: {str(e)}")
                    results.append(f"{ip}: Error: {str(e)}")

        self.logger.log_success("Execution finished.")
        return results
