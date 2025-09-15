"""
Waste routes for waste data operations
"""
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel
from typing import Optional

from controllers.waste import WasteController
from models.database import Device

router = APIRouter(prefix="/waste", tags=["🗂️ Waste Data Management"])

class WasteUpload(BaseModel):
    device_id: str
    user_qr: str
    organic: float
    recyclable: float
    hazardous: float

def verify_device_api_key(device_id: str, api_key: Optional[str] = Header(None, alias="X-API-Key")):
    """Verify device API key for authorization."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required in X-API-Key header"
        )
    
    device = Device.verify_api_key(device_id, api_key)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device ID or API key"
        )
    
    if not device['is_active']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Device is inactive"
        )
    
    return device

@router.post("/upload", status_code=201)
def upload_waste_data(
    waste_data: WasteUpload,
    api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """Upload waste data from scanning devices. Requires device API key."""
    # Verify device authorization
    verify_device_api_key(waste_data.device_id, api_key)
    
    return WasteController.upload_waste_data(
        device_id=waste_data.device_id,
        user_qr=waste_data.user_qr,
        organic=waste_data.organic,
        recyclable=waste_data.recyclable,
        hazardous=waste_data.hazardous
    )

@router.get("/{waste_id}")
def get_waste_data(waste_id: int):
    """Get waste data by ID."""
    return WasteController.get_waste_data_by_id(waste_id)
