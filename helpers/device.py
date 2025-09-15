"""
Device utilities
"""
import secrets
import string

def generate_device_api_key():
    """Generate a secure API key for devices."""
    # Generate 32-character random string
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(32))
