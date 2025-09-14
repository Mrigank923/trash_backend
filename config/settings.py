"""
Application settings and configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "300"))
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Application Settings
    APP_NAME: str = "Smart Waste Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]  # Configure for production
    
    # Rewards Settings
    ORGANIC_POINTS_PER_KG: int = 10
    RECYCLABLE_POINTS_PER_KG: int = 15
    HAZARDOUS_POINTS_PER_KG: int = 5
    
    # Email Settings
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "Smart Waste Management System")
    
    def __post_init__(self):
        """Validate required environment variables."""
        required_vars = {
            "SECRET_KEY": self.SECRET_KEY,
            "DATABASE_URL": self.DATABASE_URL,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Email settings are optional but warn if not configured
        if not self.EMAIL_USERNAME or not self.EMAIL_PASSWORD:
            print("⚠️  Warning: Email verification disabled. EMAIL_USERNAME and EMAIL_PASSWORD not configured.")

settings = Settings()
