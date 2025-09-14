"""
User routes for normal users
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models.schemas import WasteDataResponse, QRCodeResponse
from controllers.user import UserController
from middlewares.auth import require_normal_user
from models.database import UserRole

router = APIRouter(
    prefix="/user", 
    tags=["👤 User Operations"],
    dependencies=[Depends(require_normal_user)],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Normal user access required"},
        404: {"description": "Resource not found"}
    }
)

@router.get(
    "/waste", 
    response_model=List[WasteDataResponse],
    summary="Get user's waste history",
    description="""
    Retrieve the complete waste upload history for the current user.
    
    **Returns:**
    - List of all waste entries
    - Sorted by most recent first
    - Includes weight data for all waste types
    - Shows timestamp and device information
    
    **Authentication:** Requires normal user role
    """,
    responses={
        200: {
            "description": "Waste history retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "organic_weight": 2.5,
                            "recyclable_weight": 1.8,
                            "hazardous_weight": 0.3,
                            "timestamp": "2025-09-14T10:30:00",
                            "device_id": 1
                        }
                    ]
                }
            }
        }
    }
)
def get_waste_history(
    current_user = Depends(require_normal_user),
    db: Session = Depends(get_db)
):
    """Get user's waste upload history."""
    return UserController.get_waste_history(current_user, db)

@router.get(
    "/rewards",
    summary="Get user's rewards information",
    description="""
    Get comprehensive rewards information for the current user.
    
    **Returns:**
    - Total reward points
    - Rewards breakdown by waste type
    - Complete reward history
    - Points earned per waste category
    
    **Reward System:**
    - Organic waste: 10 points per kg
    - Recyclable waste: 15 points per kg
    - Hazardous waste: 5 points per kg
    """,
    responses={
        200: {
            "description": "Rewards information retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_rewards": 450,
                        "rewards_breakdown": {
                            "organic": {"total_points": 200, "total_weight": 20.0},
                            "recyclable": {"total_points": 225, "total_weight": 15.0},
                            "hazardous": {"total_points": 25, "total_weight": 5.0}
                        },
                        "reward_history": []
                    }
                }
            }
        }
    }
)
def get_user_rewards(
    current_user = Depends(require_normal_user),
    db: Session = Depends(get_db)
):
    """Get user's total rewards and reward history."""
    return UserController.get_user_rewards(current_user, db)

@router.get(
    "/qrcode", 
    response_model=QRCodeResponse,
    summary="Get user's QR code",
    description="""
    Retrieve the user's unique QR code for waste scanning devices.
    
    **QR Code Usage:**
    - Used by scanning devices to identify user
    - Required for waste data upload
    - Unique per user
    - Format: USER_XXXXXXXX
    
    **Note:** Only normal users have QR codes
    """,
    responses={
        200: {
            "description": "QR code retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "qr_code": "USER_A1B2C3D4",
                        "user_id": 123
                    }
                }
            }
        },
        404: {"description": "QR code not found"}
    }
)
def get_qr_code(current_user = Depends(require_normal_user)):
    """Get user's QR code."""
    return UserController.get_qr_code(current_user)

@router.get(
    "/stats",
    summary="Get user's waste statistics",
    description="""
    Get comprehensive waste statistics and analytics for the user.
    
    **Returns:**
    - Total waste by category
    - Total number of waste entries
    - Monthly waste trends
    - Email verification status
    - Total environmental impact
    """,
    responses={
        200: {
            "description": "User statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_organic": 45.5,
                        "total_recyclable": 32.8,
                        "total_hazardous": 8.2,
                        "total_entries": 25,
                        "monthly_stats": [
                            {"month": "2025-09", "total_weight": 86.5}
                        ],
                        "email_verified": True
                    }
                }
            }
        }
    }
)
def get_user_stats(
    current_user = Depends(require_normal_user),
    db: Session = Depends(get_db)
):
    """Get user's waste statistics."""
    return UserController.get_user_stats(current_user, db)
