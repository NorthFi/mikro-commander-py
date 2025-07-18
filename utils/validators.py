# /utils/validators.py example as follow # mikro-commander-py/utils/validators.py
"""
Validation utilities for IP addresses, command syntax, and user input.
"""

import re

def is_valid_ip(ip: str) -> bool:
    """
    Validate IPv4 address format.
    Returns True if valid, False otherwise.
    """
    # IPv4 regex: matches four groups of 1-3 digits separated by dots
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not pattern.match(ip):
        return False
    # Check each octet is 0-255
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def is_valid_port(port: str) -> bool:
    """
    Validate if string is a valid TCP port number (1-65535).
    """
    try:
        num = int(port)
        return 1 <= num <= 65535
    except ValueError:
        return False

def is_non_empty_string(value: str) -> bool:
    """
    Returns True if value is a non-empty string that is not just whitespace.
    """
    return isinstance(value, str) and value.strip() != ""
