"""
Admin routes for administrative operations
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from controllers.admin import AdminController
from middlewares.auth import get_admin_user

router = APIRouter(prefix="/admin", tags=["🔧 Admin Management"])

class DeviceCreate(BaseModel):
    device_id: str
    api_key: Optional[str] = None  # Optional - will be auto-generated if not provided

@router.get("/overview")
def get_waste_overview(current_user = Depends(get_admin_user)):
    """Get overall waste management statistics."""
    return AdminController.get_waste_overview()

@router.get("/users")
def get_all_users(current_user = Depends(get_admin_user)):
    """Get list of all users."""
    return AdminController.get_all_users()

@router.get("/devices")
def get_all_devices(current_user = Depends(get_admin_user)):
    """Get list of all registered devices."""
    return AdminController.get_all_devices()

@router.post("/device/register", status_code=201)
def register_device(
    device_data: DeviceCreate,
    current_user = Depends(get_admin_user)
):
    """Register a new scanner device."""
    return AdminController.register_device(device_data.device_id, device_data.api_key)

@router.put("/device/{device_id}/deactivate")
def deactivate_device(
    device_id: str,
    current_user = Depends(get_admin_user)
):
    """Deactivate a device."""
    return AdminController.deactivate_device(device_id)

@router.get("/user/{user_id}")
def get_user_by_id(
    user_id: int,
    current_user = Depends(get_admin_user)
):
    """Get user by ID."""
    return AdminController.get_user_by_id(user_id)

@router.delete("/user/{user_id}")
def delete_user(
    user_id: int,
    current_user = Depends(get_admin_user)
):
    """Delete a user (admin only)."""
    return AdminController.delete_user(user_id)
