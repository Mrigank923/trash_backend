"""
User routes for normal users
"""
from fastapi import APIRouter, Depends

from controllers.user import UserController
from middlewares.auth import get_current_user

router = APIRouter(prefix="/user", tags=["👤 User Operations"])

@router.get("/waste")
def get_waste_history(current_user = Depends(get_current_user)):
    """Get user's waste upload history."""
    return UserController.get_waste_history(current_user['id'])

@router.get("/demowaste")
def get_demo_waste_history():
    """Get user's demo waste upload history."""
    return UserController.get_demo_waste_history(3)


@router.get("/rewards")
def get_user_rewards(current_user = Depends(get_current_user)):
    """Get user's total rewards and reward history."""
    return UserController.get_user_rewards(current_user['id'])

@router.get("/qrcode")
def get_qr_code(current_user = Depends(get_current_user)):
    """Get user's QR code."""
    return UserController.get_qr_code(current_user['id'])

@router.get("/stats")
def get_user_stats(current_user = Depends(get_current_user)):
    """Get user's waste statistics."""
    return UserController.get_user_stats(current_user['id'])
