"""
Admin controller for administrative operations
"""
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.database import User, Device, WasteData, UserRole, Rewards, OTPVerification
from models.schemas import DeviceCreate, DeviceResponse, WasteOverview, UserResponse
from helpers.utils import generate_device_api_key

class AdminController:
    
    @staticmethod
    def get_waste_overview(db: Session) -> WasteOverview:
        """Get overall waste management statistics."""
        # Calculate total weights
        total_organic = db.query(func.sum(WasteData.organic_weight)).scalar() or 0
        total_recyclable = db.query(func.sum(WasteData.recyclable_weight)).scalar() or 0
        total_hazardous = db.query(func.sum(WasteData.hazardous_weight)).scalar() or 0
        
        # Count entities
        total_users = db.query(User).filter(User.role == UserRole.normal_user).count()
        total_devices = db.query(Device).count()
        total_waste_entries = db.query(WasteData).count()
        
        return WasteOverview(
            total_organic=float(total_organic),
            total_recyclable=float(total_recyclable),
            total_hazardous=float(total_hazardous),
            total_users=total_users,
            total_devices=total_devices,
            total_waste_entries=total_waste_entries
        )
    
    @staticmethod
    def get_all_users(db: Session) -> List[UserResponse]:
        """Get all users in the system."""
        users = db.query(User).all()
        return users
    
    @staticmethod
    def get_all_devices(db: Session) -> List[DeviceResponse]:
        """Get all registered devices."""
        devices = db.query(Device).all()
        return devices
    
    @staticmethod
    def register_device(device_data: DeviceCreate, db: Session) -> DeviceResponse:
        """Register a new device."""
        # Check if device already exists
        existing_device = db.query(Device).filter(Device.device_id == device_data.device_id).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device already registered"
            )
        
        # Create new device
        db_device = Device(
            device_id=device_data.device_id,
            api_key=device_data.api_key,
            is_active=True
        )
        
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        
        return db_device
    
    @staticmethod
    def deactivate_device(device_id: str, db: Session) -> DeviceResponse:
        """Deactivate a device."""
        device = db.query(Device).filter(Device.device_id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        
        device.is_active = False
        db.commit()
        db.refresh(device)
        
        return device
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> UserResponse:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def delete_user(user_id: int, db: Session) -> dict:
        """Delete a user (admin only)."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role == UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete admin user"
            )
        
        # Delete related records first to avoid foreign key constraint violations
        
        # Delete OTP verifications
        db.query(OTPVerification).filter(OTPVerification.user_id == user_id).delete()
        
        # Delete rewards
        db.query(Rewards).filter(Rewards.user_id == user_id).delete()
        
        # Delete waste data
        db.query(WasteData).filter(WasteData.user_id == user_id).delete()
        
        # Finally delete the user
        db.delete(user)
        db.commit()
        
        return {"message": "User deleted successfully"}
