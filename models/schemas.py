"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    normal_user = "normal_user"
    buyer = "buyer"
    admin = "admin"

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_no: str
    password: str
    role: UserRole

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_no: str
    role: UserRole
    qr_code: Optional[str] = None
    rewards: int = 0
    is_email_verified: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# Device Schemas
class DeviceCreate(BaseModel):
    device_id: str
    api_key: str

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Waste Data Schemas
class WasteUpload(BaseModel):
    device_id: str
    user_qr: str  # QR code for user identification
    organic: float = 0.0
    recyclable: float = 0.0
    hazardous: float = 0.0

class WasteDataResponse(BaseModel):
    id: int
    organic_weight: float
    recyclable_weight: float
    hazardous_weight: float
    timestamp: datetime
    device_id: int
    
    class Config:
        from_attributes = True

# Rewards Schemas
class RewardResponse(BaseModel):
    id: int
    points: int
    waste_type: str
    weight: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Admin Overview Schema
class WasteOverview(BaseModel):
    total_organic: float
    total_recyclable: float
    total_hazardous: float
    total_users: int
    total_devices: int
    total_waste_entries: int

# QR Code Response
class QRCodeResponse(BaseModel):
    qr_code: str
    user_id: int

# Error Response
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# OTP Schemas
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str

class OTPResponse(BaseModel):
    message: str
    expires_in_minutes: int = 10

class EmailVerificationResponse(BaseModel):
    message: str
    is_verified: bool
