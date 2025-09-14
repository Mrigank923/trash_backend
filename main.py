"""
Main application file for Smart Waste Management System
"""
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.database import create_tables, get_db
from config.settings import settings
from models.database import User, UserRole
from helpers.auth import get_password_hash
from middlewares.cors import add_cors_middleware

# Import routes
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.buyer import router as buyer_router
from routes.admin import router as admin_router
from routes.waste import router as waste_router

def create_admin_user():
    """Create default admin user if it doesn't exist."""
    db = next(get_db())
    try:
        admin_user = db.query(User).filter(User.role == UserRole.admin).first()
        if not admin_user:
            # Use environment variable for admin password or generate a secure one
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@wastemanagement.com")
            
            admin = User(
                name="Admin",
                email=admin_email,
                phone_no=os.getenv("ADMIN_PHONE", "+1234567890"),
                password=get_password_hash(admin_password),
                role=UserRole.admin,
                qr_code=None,
                rewards=0,
                is_email_verified=True  # Admin doesn't need email verification
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin user created: {admin_email} / {admin_password}")
            if admin_password == "admin123":
                print("⚠️  WARNING: Using default admin password. Please change it!")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Smart Waste Management API...")
    create_tables()
    create_admin_user()
    print("✅ Database initialized successfully!")
    yield
    # Shutdown
    print("🔄 Shutting down...")

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## Smart Waste Management API
    
    A comprehensive backend system for waste segregation, tracking, and recycling management.
    
    ### Features:
    * **User Management**: Registration, authentication with email verification
    * **Waste Tracking**: Upload and track organic, recyclable, and hazardous waste
    * **Reward System**: Earn points for proper waste disposal
    * **Device Integration**: Support for waste scanning devices
    * **Admin Dashboard**: Complete administrative control
    * **Buyer Portal**: Access to recyclable waste data
    
    ### Authentication:
    Most endpoints require JWT authentication. Get your token from the `/auth/login` endpoint.
    
    ### Email Verification:
    New users must verify their email address using 4-digit OTP before logging in.
    
    ### API Flow:
    1. **Register** → `/auth/register`
    2. **Get OTP** → `/auth/send-otp`
    3. **Verify Email** → `/auth/verify-otp`
    4. **Login** → `/auth/login`
    5. **Use Protected Endpoints** → Include `Authorization: Bearer <token>` header
    
    ---
    **Admin Credentials**: admin@wastemanagement.com / admin123
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    contact={
        "name": "Smart Waste Management Team",
        "email": "admin@wastemanagement.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.smartwaste.com",
            "description": "Production server"
        }
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
        "displayRequestDuration": True,
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
    }
)

# Add CORS middleware
add_cors_middleware(app)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(buyer_router)
app.include_router(admin_router)
app.include_router(waste_router)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "admin_credentials": "admin@wastemanagement.com / admin123"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.DEBUG
    )
