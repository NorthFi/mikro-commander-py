# /utils/file_ops.py example as follow # mikro-commander-py/utils/file_ops.py
"""
File operations utilities for reading/writing lists and text files.
"""

from typing import List

def read_ip_list(file_path: str) -> List[str]:
    """
    Read a text file and return a list of non-empty lines (IP addresses).
    Strips whitespace and ignores empty lines.
    """
    ips = []
    with open(file_path, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                ips.append(ip)
    return ips

def write_output(file_path: str, output: str) -> None:
    """
    Write a string output to the specified file.
    Overwrites existing content.
    """
    with open(file_path, "w") as f:
        f.write(output)
