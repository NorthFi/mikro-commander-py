# /tests/test_validators.py example as follow # mikro-commander-py/tests/test_validators.py
"""
Unit tests for validation utilities in utils/validators.py.
"""

from utils.validators import is_valid_ip, is_valid_port, is_non_empty_string

def test_valid_ip():
    assert is_valid_ip("192.168.1.1")
    assert not is_valid_ip("999.999.999.999")
    assert not is_valid_ip("abc.def.1.1")

def test_valid_port():
    assert is_valid_port("22")
    assert is_valid_port("65535")
    assert not is_valid_port("0")
    assert not is_valid_port("70000")
    assert not is_valid_port("not_a_port")

def test_non_empty_string():
    assert is_non_empty_string("hello")
    assert not is_non_empty_string("")
    assert not is_non_empty_string("   ")
