"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from controllers.auth import register_user, login_user, send_otp_email, verify_otp_code
from middlewares.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["🔐 Authentication"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_no: str
    password: str
    role: str = "normal_user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    """Register a new user."""
    return register_user(
        name=user_data.name,
        email=user_data.email,
        phone_no=user_data.phone_no,
        password=user_data.password,
        role=user_data.role
    )

@router.post("/login")
def login(user_data: UserLogin):
    """Login user."""
    return login_user(user_data.email, user_data.password)

@router.post("/send-otp")
def send_otp(otp_request: OTPRequest):
    """Send OTP for email verification."""
    return send_otp_email(otp_request.email)

@router.post("/verify-otp")
def verify_otp(otp_data: OTPVerify):
    """Verify OTP code."""
    return verify_otp_code(otp_data.email, otp_data.otp_code)

@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user information."""
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "qr_code": current_user["qr_code"],
        "rewards": current_user["rewards"],
        "is_email_verified": current_user["is_email_verified"]
    }
