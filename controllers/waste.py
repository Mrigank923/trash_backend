"""
Waste controller for waste data operations
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.database import WasteData, Device, User, Rewards
from models.schemas import WasteUpload, WasteDataResponse
from helpers.utils import calculate_reward_points, validate_weights

class WasteController:
    
    @staticmethod
    def upload_waste_data(waste_data: WasteUpload, db: Session) -> WasteDataResponse:
        """Upload waste data from scanning devices."""
        # Validate device exists and is active
        device = db.query(Device).filter(
            Device.device_id == waste_data.device_id,
            Device.is_active == True
        ).first()
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found or inactive"
            )
        
        # Find user by QR code
        user = db.query(User).filter(User.qr_code == waste_data.user_qr).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please check QR code."
            )
        
        # Validate waste weights
        if not validate_weights(waste_data.organic, waste_data.recyclable, waste_data.hazardous):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Waste weights must be non-negative"
            )
        
        # Create waste data entry
        db_waste = WasteData(
            user_id=user.id,
            device_id=device.id,
            organic_weight=waste_data.organic,
            recyclable_weight=waste_data.recyclable,
            hazardous_weight=waste_data.hazardous
        )
        
        db.add(db_waste)
        db.commit()
        db.refresh(db_waste)
        
        # Calculate and award points
        points_breakdown = calculate_reward_points(
            waste_data.organic, 
            waste_data.recyclable, 
            waste_data.hazardous
        )
        
        total_points = points_breakdown["total_points"]
        
        if total_points > 0:
            # Add individual reward entries for each waste type
            if waste_data.organic > 0:
                organic_reward = Rewards(
                    user_id=user.id,
                    points=points_breakdown["organic_points"],
                    waste_type="organic",
                    weight=waste_data.organic
                )
                db.add(organic_reward)
            
            if waste_data.recyclable > 0:
                recyclable_reward = Rewards(
                    user_id=user.id,
                    points=points_breakdown["recyclable_points"],
                    waste_type="recyclable",
                    weight=waste_data.recyclable
                )
                db.add(recyclable_reward)
            
            if waste_data.hazardous > 0:
                hazardous_reward = Rewards(
                    user_id=user.id,
                    points=points_breakdown["hazardous_points"],
                    waste_type="hazardous",
                    weight=waste_data.hazardous
                )
                db.add(hazardous_reward)
            
            # Update user's total rewards
            user.rewards += total_points
            db.commit()
        
        return db_waste
    
    @staticmethod
    def get_waste_data_by_id(waste_id: int, db: Session) -> WasteDataResponse:
        """Get waste data by ID."""
        waste_data = db.query(WasteData).filter(WasteData.id == waste_id).first()
        if not waste_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Waste data not found"
            )
        return waste_data
