"""
Utility functions for the application
"""
import uuid
from typing import Optional

def generate_qr_code(user_id: int, role: str) -> Optional[str]:
    """Generate a unique QR code for a user."""
    if role == "normal_user":
        return f"USER_{str(uuid.uuid4())[:8].upper()}"
    return None

def generate_device_api_key() -> str:
    """Generate a secure API key for devices."""
    return f"DEV_{str(uuid.uuid4()).replace('-', '').upper()}"

def calculate_reward_points(organic_weight: float, recyclable_weight: float, hazardous_weight: float) -> dict:
    """Calculate reward points based on waste weights."""
    from config.settings import settings
    
    organic_points = int(organic_weight * settings.ORGANIC_POINTS_PER_KG)
    recyclable_points = int(recyclable_weight * settings.RECYCLABLE_POINTS_PER_KG)
    hazardous_points = int(hazardous_weight * settings.HAZARDOUS_POINTS_PER_KG)
    
    return {
        "organic_points": organic_points,
        "recyclable_points": recyclable_points,
        "hazardous_points": hazardous_points,
        "total_points": organic_points + recyclable_points + hazardous_points
    }

def format_response(data, message: str = "Success", status_code: int = 200):
    """Format API response consistently."""
    return {
        "status_code": status_code,
        "message": message,
        "data": data
    }

def validate_weights(organic: float, recyclable: float, hazardous: float) -> bool:
    """Validate that waste weights are non-negative."""
    return all(weight >= 0 for weight in [organic, recyclable, hazardous])

def get_total_waste_weight(organic: float, recyclable: float, hazardous: float) -> float:
    """Calculate total waste weight."""
    return organic + recyclable + hazardous
