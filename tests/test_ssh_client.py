# /tests/test_ssh_client.py example as follow # mikro-commander-py/tests/test_ssh_client.py
"""
Unit tests for SSHClient class in core/ssh_client.py.
Uses mocking to avoid real SSH connections.
"""

import pytest
from unittest.mock import MagicMock, patch
from core.ssh_client import SSHClient

class DummyLogger:
    def log_info(self, msg): pass
    def log_error(self, msg): pass

def test_connect_success():
    # Patch paramiko.SSHClient.connect to not actually connect
    with patch("paramiko.SSHClient.connect") as mock_connect, \
         patch("paramiko.SSHClient.__init__", return_value=None):
        logger = DummyLogger()
        client = SSHClient("127.0.0.1", "user", "pass", 22, False, logger)
        client.client = MagicMock()
        mock_connect.return_value = None
        assert client.connect() is True

def test_connect_failure():
    with patch("paramiko.SSHClient.connect", side_effect=Exception("fail")), \
         patch("paramiko.SSHClient.__init__", return_value=None):
        logger = DummyLogger()
        client = SSHClient("bad.ip", "user", "pass", 22, False, logger)
        client.client = MagicMock()
        assert client.connect() is False

def test_execute_returns_output():
    with patch("paramiko.SSHClient.exec_command") as mock_exec:
        logger = DummyLogger()
        client = SSHClient("127.0.0.1", "user", "pass", 22, False, logger)
        client.client = MagicMock()
        mock_stdout = MagicMock()
        mock_stdout.read.return_value = b"result"
        mock_stderr = MagicMock()
        mock_stderr.read.return_value = b""
        mock_exec.return_value = (None, mock_stdout, mock_stderr)
        client.client.exec_command = mock_exec
        assert client.execute("echo test") == "result"
