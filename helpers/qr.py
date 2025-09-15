"""
QR Code generation utilities
"""
import secrets
import string

def generate_qr_code():
    """Generate a unique QR code for users."""
    # Generate 8 character random string
    characters = string.ascii_uppercase + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(8))
    return f"USER_{random_string}"
