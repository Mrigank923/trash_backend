"""
Database models for the Smart Waste Management System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from config.database import Base

class UserRole(enum.Enum):
    normal_user = "normal_user"
    buyer = "buyer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_no = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    qr_code = Column(String, unique=True, nullable=True)
    rewards = Column(Integer, default=0)
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    waste_data = relationship("WasteData", back_populates="user")
    user_rewards = relationship("Rewards", back_populates="user")
    otp_verifications = relationship("OTPVerification", back_populates="user")

class OTPVerification(Base):
    __tablename__ = "otp_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email = Column(String, nullable=False)
    otp_code = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="otp_verifications")

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    api_key = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    waste_data = relationship("WasteData", back_populates="device")

class WasteData(Base):
    __tablename__ = "waste_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    organic_weight = Column(Float, default=0.0)
    recyclable_weight = Column(Float, default=0.0)
    hazardous_weight = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="waste_data")
    device = relationship("Device", back_populates="waste_data")

class Rewards(Base):
    __tablename__ = "rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)
    waste_type = Column(String, nullable=False)  # organic, recyclable, hazardous
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_rewards")
