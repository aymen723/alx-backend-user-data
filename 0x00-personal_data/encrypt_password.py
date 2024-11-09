#!/usr/bin/env python3
"""
Provides functions to hash passwords and verify their validity
"""
import bcrypt
from bcrypt import hashpw

def generate_hashed_password(plain_text_password: str) -> bytes:
    """
    Generates a hashed version of a given password.
    
    Args:
        plain_text_password (str): The password to be hashed.
    
    Returns:
        bytes: The hashed password in bytes.
    """
    encoded_password = plain_text_password.encode()  # Convert the password to bytes
    hashed_password = hashpw(encoded_password, bcrypt.gensalt())  # Hash the password with a salt
    return hashed_password

def verify_password(hashed_password: bytes, plain_text_password: str) -> bool:
    """
    Validates a plain text password against a hashed password.
    
    Args:
        hashed_password (bytes): The hashed password to verify against.
        plain_text_password (str): The plain text password to check.
    
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)  # Compare hashed and plain text passwords
