"""
Waste routes for waste data operations
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.schemas import WasteUpload, WasteDataResponse
from controllers.waste import WasteController

router = APIRouter(
    prefix="/waste", 
    tags=["🗂️ Waste Data Management"],
    responses={
        400: {"description": "Invalid request data"},
        404: {"description": "Resource not found"},
        422: {"description": "Validation error"}
    }
)

@router.post(
    "/upload", 
    response_model=WasteDataResponse, 
    status_code=201,
    summary="Upload waste scanning data",
    description="""
    Process and record waste data from scanning devices.
    
    **Waste Upload Process:**
    - Validate QR code and user identity
    - Validate device exists and is active
    - Record waste measurements by category
    - Calculate environmental impact metrics
    - Award user reward points automatically
    - Update device usage statistics
    
    **Required Data:**
    - Valid user QR code (format: USER_XXXXXXXX)
    - Device identifier
    - Weight measurements for waste categories:
      - Organic waste (compostable materials)
      - Recyclable waste (reusable materials)  
      - Hazardous waste (special handling required)
    
    **Automatic Processing:**
    - Real-time data validation
    - Reward point calculation and assignment
    - Environmental impact tracking
    - System statistics updates
    
    **Reward System:**
    - Organic waste: 10 points per kg
    - Recyclable waste: 15 points per kg
    - Hazardous waste: 5 points per kg
    """,
    responses={
        201: {
            "description": "Waste data uploaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "user_id": 456,
                        "device_id": "DEVICE001",
                        "organic_weight": 2.5,
                        "recyclable_weight": 1.8,
                        "hazardous_weight": 0.3,
                        "timestamp": "2025-09-14T10:30:00",
                        "points_awarded": 57,
                        "environmental_impact": {
                            "carbon_saved": 1.2,
                            "landfill_diverted": 4.6
                        }
                    }
                }
            }
        },
        400: {"description": "Invalid QR code or device"},
        404: {"description": "User or device not found"},
        422: {"description": "Invalid weight measurements"}
    }
)
def upload_waste_data(waste_data: WasteUpload, db: Session = Depends(get_db)):
    """Upload waste data from scanning devices."""
    return WasteController.upload_waste_data(waste_data, db)

@router.get(
    "/{waste_id}", 
    response_model=WasteDataResponse,
    summary="Get waste entry details",
    description="""
    Retrieve detailed information for a specific waste data entry.
    
    **Waste Entry Details:**
    - Complete waste measurement data
    - User and device identification
    - Timestamp and location information
    - Environmental impact calculations
    - Reward points awarded
    
    **Data Verification:**
    - Authentic waste submission records
    - Audit trail for compliance
    - Quality assurance validation
    - Data integrity verification
    
    **Use Cases:**
    - Data verification and auditing
    - User support and troubleshooting
    - Environmental impact reporting
    - System analytics and research
    
    **Returned Information:**
    - Waste categorization and weights
    - Processing timestamps
    - Associated user and device data
    - Calculated environmental benefits
    """,
    responses={
        200: {
            "description": "Waste data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "user_id": 456,
                        "device_id": "DEVICE001",
                        "organic_weight": 2.5,
                        "recyclable_weight": 1.8,
                        "hazardous_weight": 0.3,
                        "timestamp": "2025-09-14T10:30:00",
                        "points_awarded": 57,
                        "verification_status": "verified"
                    }
                }
            }
        },
        404: {"description": "Waste entry not found"}
    }
)
def get_waste_data(waste_id: int, db: Session = Depends(get_db)):
    """Get waste data by ID."""
    return WasteController.get_waste_data_by_id(waste_id, db)
