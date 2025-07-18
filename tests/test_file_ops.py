# /tests/test_file_ops.py example as follow # mikro-commander-py/tests/test_file_ops.py
"""
Unit tests for file operations in utils/file_ops.py.
"""

import tempfile
from utils.file_ops import read_ip_list, write_output

def test_read_ip_list():
    # Write some IPs to a temp file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("192.168.1.1\n10.0.0.2\n\n")
        tmp.flush()
        ips = read_ip_list(tmp.name)
    assert ips == ["192.168.1.1", "10.0.0.2"]

def test_write_output():
    # Write and read from a temp file
    with tempfile.NamedTemporaryFile(mode="r+", delete=False) as tmp:
        file_path = tmp.name
        write_output(file_path, "output text")
        tmp.seek(0)
        content = tmp.read()
    assert content == "output text"
