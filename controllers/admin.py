"""
Admin controller for administrative operations
"""
from fastapi import HTTPException, status

from models.database import User, Device, WasteData, execute_query
from helpers.device import generate_device_api_key

class AdminController:
    
    @staticmethod
    def get_waste_overview():
        """Get overall waste management statistics."""
        # Calculate total weights
        total_organic_query = "SELECT COALESCE(SUM(organic_weight), 0) FROM waste_data"
        total_recyclable_query = "SELECT COALESCE(SUM(recyclable_weight), 0) FROM waste_data"
        total_hazardous_query = "SELECT COALESCE(SUM(hazardous_weight), 0) FROM waste_data"
        
        total_organic = execute_query(total_organic_query, fetch='one')['coalesce']
        total_recyclable = execute_query(total_recyclable_query, fetch='one')['coalesce']
        total_hazardous = execute_query(total_hazardous_query, fetch='one')['coalesce']
        
        # Count entities
        total_users = execute_query("SELECT COUNT(*) FROM users WHERE role = 'normal_user'", fetch='one')['count']
        total_devices = execute_query("SELECT COUNT(*) FROM devices", fetch='one')['count']
        total_waste_entries = execute_query("SELECT COUNT(*) FROM waste_data", fetch='one')['count']
        
        return {
            "total_organic": float(total_organic),
            "total_recyclable": float(total_recyclable),
            "total_hazardous": float(total_hazardous),
            "total_users": total_users,
            "total_devices": total_devices,
            "total_waste_entries": total_waste_entries
        }
    
    @staticmethod
    def get_all_users():
        """Get all users in the system."""
        return User.get_all()
    
    @staticmethod
    def get_all_devices():
        """Get all registered devices."""
        query = "SELECT * FROM devices ORDER BY created_at DESC"
        return execute_query(query, fetch='all')
    
    @staticmethod
    def register_device(device_id: str, api_key: str = None):
        """Register a new device."""
        # Check if device already exists
        existing_device = Device.get_by_device_id(device_id)
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Device already registered"
            )
        
        # Generate API key if not provided
        if not api_key:
            api_key = generate_device_api_key()
        
        # Create new device
        query = """
        INSERT INTO devices (device_id, api_key, is_active)
        VALUES (%(device_id)s, %(api_key)s, %(is_active)s)
        RETURNING *
        """
        params = {
            'device_id': device_id,
            'api_key': api_key,
            'is_active': True
        }
        device = execute_query(query, params, fetch='one')
        
        # Return device info including API key (only shown once during registration)
        return {
            "device_id": device['device_id'],
            "api_key": api_key,
            "is_active": device['is_active'],
            "created_at": device['created_at'],
            "message": "Device registered successfully. Save the API key securely - it won't be shown again."
        }
    
    @staticmethod
    def deactivate_device(device_id: str):
        """Deactivate a device."""
        device = Device.get_by_device_id(device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found"
            )
        
        query = "UPDATE devices SET is_active = FALSE WHERE device_id = %(device_id)s RETURNING *"
        return execute_query(query, {'device_id': device_id}, fetch='one')
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """Get user by ID."""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def delete_user(user_id: int):
        """Delete a user (admin only)."""
        user = User.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user['role'] == 'admin':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete admin user"
            )
        
        # Delete the user (foreign key constraints will handle related records)
        query = "DELETE FROM users WHERE id = %(user_id)s"
        execute_query(query, {'user_id': user_id})
        
        return {"message": "User deleted successfully"}
