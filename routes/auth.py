"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    OTPRequest, OTPVerify, OTPResponse, EmailVerificationResponse
)
from controllers.auth import AuthController
from controllers.otp import OTPController
from middlewares.auth import get_current_user

router = APIRouter(
    prefix="/auth", 
    tags=["🔐 Authentication"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    }
)

@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
    Register a new user account. Only 'normal_user' and 'buyer' roles are allowed.
    
    **Steps after registration:**
    1. User receives registration confirmation
    2. Send OTP to email using `/auth/send-otp`
    3. Verify email with OTP using `/auth/verify-otp`
    4. Login using `/auth/login`
    
    **Note**: Email verification is required before login.
    """,
    responses={
        201: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john@example.com",
                        "phone_no": "+1234567890",
                        "role": "normal_user",
                        "qr_code": "USER_A1B2C3D4",
                        "rewards": 0,
                        "is_email_verified": False,
                        "created_at": "2025-09-14T10:30:00"
                    }
                }
            }
        },
        400: {"description": "Email already registered or invalid role"}
    }
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (normal_user or buyer only). Email verification required before login."""
    return AuthController.register_user(user_data, db)

@router.post(
    "/send-otp", 
    response_model=OTPResponse,
    summary="Send OTP for email verification",
    description="""
    Send a 4-digit OTP code to the user's email for verification.
    
    **Requirements:**
    - User must be registered
    - Email must not be already verified
    
    **OTP Details:**
    - 4-digit numeric code
    - Valid for 10 minutes
    - Single use only
    
    **Email Configuration:**
    If email is not configured, OTP will be printed to server console.
    """,
    responses={
        200: {
            "description": "OTP sent successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "OTP sent successfully to your email",
                        "expires_in_minutes": 10
                    }
                }
            }
        },
        400: {"description": "Email already verified"},
        404: {"description": "User not found"},
        500: {"description": "Failed to send email"}
    }
)
def send_verification_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    """Send OTP to email for verification."""
    return OTPController.send_verification_otp(otp_request, db)

@router.post(
    "/verify-otp", 
    response_model=EmailVerificationResponse,
    summary="Verify email with OTP",
    description="""
    Verify the OTP code and mark email as verified.
    
    **Requirements:**
    - Valid OTP code (4 digits)
    - OTP must not be expired (within 10 minutes)
    - OTP must not be already used
    
    **After successful verification:**
    - Email is marked as verified
    - User can now login
    - OTP becomes invalid
    """,
    responses={
        200: {
            "description": "Email verified successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Email verified successfully",
                        "is_verified": True
                    }
                }
            }
        },
        400: {"description": "Invalid, expired, or already used OTP"},
        404: {"description": "User not found"}
    }
)
def verify_email_otp(otp_verify: OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and activate email."""
    return OTPController.verify_otp(otp_verify, db)

@router.post(
    "/resend-otp", 
    response_model=OTPResponse,
    summary="Resend OTP for email verification",
    description="""
    Resend a new OTP code if the previous one expired or was lost.
    
    **This will:**
    - Invalidate any existing unused OTPs
    - Generate a new 4-digit OTP
    - Send new OTP to email
    - New OTP valid for 10 minutes
    """,
    responses={
        200: {"description": "New OTP sent successfully"},
        400: {"description": "Email already verified"},
        404: {"description": "User not found"}
    }
)
def resend_verification_otp(otp_request: OTPRequest, db: Session = Depends(get_db)):
    """Resend OTP to email for verification."""
    return OTPController.resend_otp(otp_request, db)

@router.post(
    "/login", 
    response_model=Token,
    summary="User login",
    description="""
    Authenticate user and receive JWT access token.
    
    **Requirements:**
    - Valid email and password
    - Email must be verified (except for admin users)
    
    **Response:**
    - JWT access token
    - Token type (Bearer)
    
    **Token Usage:**
    Include in headers: `Authorization: Bearer <access_token>`
    """,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {"description": "Incorrect email or password"},
        403: {"description": "Email not verified"}
    }
)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token. Email must be verified."""
    return AuthController.login_user(user_credentials, db)

@router.get(
    "/me", 
    response_model=UserResponse,
    summary="Get current user profile",
    description="""
    Get the profile information of the currently authenticated user.
    
    **Authentication Required:** Bearer token in header
    
    **Returns:**
    - User profile details
    - Email verification status
    - Current reward points
    - QR code (for normal users)
    """,
    responses={
        200: {"description": "User profile retrieved successfully"},
        401: {"description": "Invalid or missing token"},
        404: {"description": "User not found"}
    }
)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user information."""
    return AuthController.get_user_profile(current_user)
