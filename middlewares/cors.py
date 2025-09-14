"""
CORS middleware configuration
"""
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

def add_cors_middleware(app):
    """Add CORS middleware to the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
