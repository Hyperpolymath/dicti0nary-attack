"""
dicti0nary-attack: A security research utility for testing non-dictionary passwords.

This tool is designed for authorized security testing, penetration testing,
CTF competitions, and educational purposes only.

WARNING: Unauthorized access to computer systems is illegal. Always obtain
explicit written permission before testing any system you do not own.
"""

__version__ = "0.1.0"
__author__ = "Security Research Team"
__license__ = "GPL-3.0"

from dicti0nary_attack.generators.base import PasswordGenerator
from dicti0nary_attack.generators.leetspeak import LeetspeakGenerator
from dicti0nary_attack.generators.phonetic import PhoneticGenerator
from dicti0nary_attack.generators.pattern import PatternGenerator
from dicti0nary_attack.crackers.hash_cracker import HashCracker

__all__ = [
    "PasswordGenerator",
    "LeetspeakGenerator",
    "PhoneticGenerator",
    "PatternGenerator",
    "HashCracker",
]
