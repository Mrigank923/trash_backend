"""
Admin routes for administrative operations
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models.schemas import DeviceCreate, DeviceResponse, UserResponse, WasteOverview
from controllers.admin import AdminController
from middlewares.auth import require_admin

router = APIRouter(
    prefix="/admin", 
    tags=["🔧 Admin Management"],
    dependencies=[Depends(require_admin)],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Admin access required"},
        404: {"description": "Resource not found"}
    }
)

@router.get(
    "/overview", 
    response_model=WasteOverview,
    summary="Get system waste overview",
    description="""
    Retrieve comprehensive waste management statistics and system overview.
    
    **System Metrics:**
    - Total waste collected by category
    - Active users and devices
    - Collection efficiency rates
    - Environmental impact metrics
    
    **Key Performance Indicators:**
    - Daily/monthly collection trends
    - Waste diversion rates
    - User engagement levels
    - Device utilization statistics
    
    **Admin Dashboard Data:**
    - Real-time system health
    - Performance benchmarks
    - Compliance metrics
    """,
    responses={
        200: {
            "description": "Waste overview retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_organic": 2500.5,
                        "total_recyclable": 1800.3,
                        "total_hazardous": 450.2,
                        "total_users": 1500,
                        "active_devices": 48,
                        "collection_efficiency": 87.5
                    }
                }
            }
        }
    }
)
def get_waste_overview(
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get overall waste management statistics."""
    return AdminController.get_waste_overview(db)

@router.get(
    "/users", 
    response_model=List[UserResponse],
    summary="Get all system users",
    description="""
    Retrieve comprehensive list of all registered users in the system.
    
    **User Management Features:**
    - View complete user directory
    - Monitor user activity and engagement
    - Track email verification status
    - Access user registration data
    
    **Returned Information:**
    - User credentials and contact details
    - Registration timestamps
    - Email verification status
    - Role assignments
    - Account activity metrics
    
    **Admin Capabilities:**
    - User account oversight
    - Support and troubleshooting
    - Compliance monitoring
    """,
    responses={
        200: {
            "description": "Users retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john@example.com",
                            "email_verified": True,
                            "role": "normal",
                            "created_at": "2025-01-01T10:00:00"
                        }
                    ]
                }
            }
        }
    }
)
def get_all_users(
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get list of all users."""
    return AdminController.get_all_users(db)

@router.get(
    "/devices", 
    response_model=List[DeviceResponse],
    summary="Get all scanning devices",
    description="""
    Retrieve comprehensive information about all waste scanning devices.
    
    **Device Management:**
    - Monitor device operational status
    - Track device locations and assignments
    - View device performance metrics
    - Manage device configurations
    
    **Device Information:**
    - Unique device identifiers
    - Installation locations
    - Operational status (active/inactive)
    - Last activity timestamps
    - Usage statistics and performance data
    
    **Maintenance Features:**
    - Device health monitoring
    - Maintenance scheduling
    - Performance optimization
    """,
    responses={
        200: {
            "description": "Devices retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "DEVICE001",
                            "name": "Main Campus Scanner",
                            "location": "Building A - Ground Floor",
                            "is_active": True,
                            "last_activity": "2025-09-14T15:30:00"
                        }
                    ]
                }
            }
        }
    }
)
def get_all_devices(
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get list of all registered devices."""
    return AdminController.get_all_devices(db)

@router.post(
    "/device/register", 
    response_model=DeviceResponse, 
    status_code=201,
    summary="Register new scanning device",
    description="""
    Register a new waste scanning device in the system.
    
    **Device Registration Process:**
    - Assign unique device identifier
    - Configure device parameters
    - Set installation location
    - Initialize device settings
    
    **Required Information:**
    - Device name and description
    - Installation location details
    - Initial configuration parameters
    - Operational parameters
    
    **Post-Registration:**
    - Device becomes available for waste scanning
    - Admin can monitor device status
    - Device appears in system inventory
    """,
    responses={
        201: {
            "description": "Device registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "DEVICE002",
                        "name": "Library Scanner",
                        "location": "Main Library - Entrance",
                        "is_active": True,
                        "created_at": "2025-09-14T16:00:00"
                    }
                }
            }
        },
        400: {"description": "Invalid device data"},
        409: {"description": "Device already exists"}
    }
)
def register_device(
    device_data: DeviceCreate,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Register a new scanner device."""
    return AdminController.register_device(device_data, db)

@router.put(
    "/device/{device_id}/deactivate", 
    response_model=DeviceResponse,
    summary="Deactivate scanning device",
    description="""
    Deactivate a waste scanning device, removing it from active service.
    
    **Deactivation Process:**
    - Mark device as inactive
    - Prevent new waste submissions
    - Preserve historical data
    - Update system inventory
    
    **Impact of Deactivation:**
    - Device stops accepting scans
    - Historical data remains accessible
    - Can be reactivated if needed
    - User notifications about unavailability
    
    **Use Cases:**
    - Maintenance periods
    - Device relocation
    - Equipment replacement
    - Temporary service suspension
    """,
    responses={
        200: {
            "description": "Device deactivated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "DEVICE001",
                        "name": "Main Campus Scanner",
                        "is_active": False,
                        "deactivated_at": "2025-09-14T16:30:00"
                    }
                }
            }
        },
        404: {"description": "Device not found"},
        400: {"description": "Device already inactive"}
    }
)
def deactivate_device(
    device_id: str,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Deactivate a device."""
    return AdminController.deactivate_device(device_id, db)

@router.get(
    "/user/{user_id}", 
    response_model=UserResponse,
    summary="Get user details by ID",
    description="""
    Retrieve detailed information for a specific user by their ID.
    
    **User Information Access:**
    - Complete user profile data
    - Account status and verification
    - Activity history and patterns
    - Waste submission statistics
    
    **Admin Use Cases:**
    - User support and troubleshooting
    - Account verification assistance
    - Investigation and compliance
    - Performance analysis
    
    **Detailed User Data:**
    - Personal information and credentials
    - Email verification status
    - Registration and activity timestamps
    - Role and permission levels
    """,
    responses={
        200: {
            "description": "User details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "username": "john_doe",
                        "email": "john@example.com",
                        "email_verified": True,
                        "role": "normal",
                        "created_at": "2025-01-01T10:00:00",
                        "qr_code": "USER_A1B2C3D4"
                    }
                }
            }
        },
        404: {"description": "User not found"}
    }
)
def get_user_by_id(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user by ID."""
    return AdminController.get_user_by_id(user_id, db)

@router.delete(
    "/user/{user_id}",
    summary="Delete user account",
    description="""
    Permanently delete a user account from the system.
    
    **⚠️ WARNING: This action is irreversible!**
    
    **Deletion Process:**
    - Remove user account completely
    - Delete associated waste data
    - Remove reward history
    - Invalidate QR codes
    - Clean up all user references
    
    **Data Handling:**
    - Complete data removal for privacy compliance
    - Historical data anonymization options
    - Audit trail maintenance
    - GDPR compliance procedures
    
    **Admin Responsibilities:**
    - Verify deletion necessity
    - Ensure proper authorization
    - Document deletion reasons
    - Follow company policies
    
    **Use Cases:**
    - User account closure requests
    - Data privacy compliance
    - Policy violation enforcement
    - System cleanup operations
    """,
    responses={
        200: {
            "description": "User deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User account and all associated data deleted successfully",
                        "deleted_user_id": 123,
                        "deletion_timestamp": "2025-09-14T17:00:00"
                    }
                }
            }
        },
        404: {"description": "User not found"},
        400: {"description": "Cannot delete admin users"},
        403: {"description": "Insufficient permissions for deletion"}
    }
)
def delete_user(
    user_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)."""
    return AdminController.delete_user(user_id, db)
