"""
Authentication controllers
"""
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
import secrets

from models.database import User, OTP
from helpers.auth import verify_password, get_password_hash, create_access_token
from helpers.email import send_email
from helpers.qr import generate_qr_code

def register_user(name: str, email: str, phone_no: str, password: str, role: str = "normal_user"):
    """Register a new user."""
    # Check if user exists
    existing_user = User.get_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(password)
    
    # Generate QR code for normal users
    qr_code = None
    if role == "normal_user":
        qr_code = generate_qr_code()
    
    # Create user
    user = User.create(
        name=name,
        email=email,
        phone_no=phone_no,
        password=hashed_password,
        role=role,
        qr_code=qr_code
    )
    
    return user

def authenticate_user(email: str, password: str):
    """Authenticate user with email and password."""
    user = User.get_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user['password']):
        return None
    
    return user

def login_user(email: str, password: str):
    """Login user and return access token."""
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user['is_email_verified']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified. Please verify your email first."
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user['email']})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "role": user['role'],
            "qr_code": user['qr_code'],
            "rewards": user['rewards']
        }
    }

def send_otp_email(email: str):
    """Send OTP to user email."""
    user = User.get_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user['is_email_verified']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate 4-digit OTP
    otp_code = str(secrets.randbelow(9000) + 1000)
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Save OTP
    OTP.create(
        user_id=user['id'],
        email=email,
        otp_code=otp_code,
        expires_at=expires_at
    )
    
    # Send email
    subject = "Email Verification - Smart Waste Management"
    body = f"""
    Dear {user['name']},
    
    Your email verification code is: {otp_code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this verification, please ignore this email.
    
    Best regards,
    Smart Waste Management Team
    """
    
    send_email(email, subject, body)
    
    return {"message": "OTP sent successfully"}

def verify_otp_code(email: str, otp_code: str):
    """Verify OTP code."""
    # Get valid OTP
    otp_record = OTP.verify(email, otp_code)
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Mark OTP as used
    OTP.mark_used(otp_record['id'])
    
    # Mark user email as verified
    User.verify_email(otp_record['user_id'])
    
    return {"message": "Email verified successfully"}
