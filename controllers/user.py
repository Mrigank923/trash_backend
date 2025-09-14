"""
User controller for user-specific operations
"""
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.database import User, WasteData, Rewards
from models.schemas import WasteDataResponse, RewardResponse, QRCodeResponse

class UserController:
    
    @staticmethod
    def get_waste_history(user: User, db: Session) -> List[WasteDataResponse]:
        """Get user's waste upload history."""
        waste_data = db.query(WasteData).filter(WasteData.user_id == user.id).order_by(WasteData.timestamp.desc()).all()
        return waste_data
    
    @staticmethod
    def get_user_rewards(user: User, db: Session) -> dict:
        """Get user's total rewards and reward history."""
        total_rewards = user.rewards
        reward_history = db.query(Rewards).filter(Rewards.user_id == user.id).order_by(Rewards.created_at.desc()).all()
        
        return {
            "total_rewards": total_rewards,
            "reward_history": reward_history
        }
    
    @staticmethod
    def get_qr_code(user: User) -> QRCodeResponse:
        """Get user's QR code."""
        if not user.qr_code:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR code not found for this user"
            )
        
        return QRCodeResponse(qr_code=user.qr_code, user_id=user.id)
    
    @staticmethod
    def get_user_stats(user: User, db: Session) -> dict:
        """Get user's waste statistics."""
        waste_data = db.query(WasteData).filter(WasteData.user_id == user.id).all()
        
        total_organic = sum(data.organic_weight for data in waste_data)
        total_recyclable = sum(data.recyclable_weight for data in waste_data)
        total_hazardous = sum(data.hazardous_weight for data in waste_data)
        total_entries = len(waste_data)
        
        return {
            "total_organic": total_organic,
            "total_recyclable": total_recyclable,
            "total_hazardous": total_hazardous,
            "total_weight": total_organic + total_recyclable + total_hazardous,
            "total_entries": total_entries,
            "total_rewards": user.rewards
        }
