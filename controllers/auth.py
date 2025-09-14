"""
Authentication controller for user registration and login
"""
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.database import User, UserRole
from models.schemas import UserCreate, UserLogin, Token
from helpers.auth import get_password_hash, verify_password, create_access_token
from helpers.utils import generate_qr_code
from config.settings import settings

class AuthController:
    
    @staticmethod
    def register_user(user_data: UserCreate, db: Session) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone number already exists
        existing_phone = db.query(User).filter(User.phone_no == user_data.phone_no).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Only allow normal_user and buyer registration
        if user_data.role.value not in ["normal_user", "buyer"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role. Only normal_user and buyer can register."
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        
        # Convert Pydantic enum to SQLAlchemy enum
        db_role = UserRole(user_data.role.value)
        
        db_user = User(
            name=user_data.name,
            email=user_data.email,
            phone_no=user_data.phone_no,
            password=hashed_password,
            role=db_role,
            qr_code=None,  # Will be set after user creation
            rewards=0,
            is_email_verified=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Generate QR code for normal users only (after user ID is available)
        if user_data.role.value == "normal_user":
            db_user.qr_code = generate_qr_code(db_user.id, user_data.role.value)
            db.commit()
            db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def login_user(user_credentials: UserLogin, db: Session) -> Token:
        """Authenticate user and return JWT token."""
        user = db.query(User).filter(User.email == user_credentials.email).first()
        
        if not user or not verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if email is verified for non-admin users
        if user.role != UserRole.admin and not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in. Check your inbox for the verification code."
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
    
    @staticmethod
    def get_user_profile(user: User) -> User:
        """Get user profile information."""
        return user
