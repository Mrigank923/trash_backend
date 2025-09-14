"""
Buyer controller for buyer-specific operations
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.database import WasteData, User

class BuyerController:
    
    @staticmethod
    def get_available_recyclables(db: Session) -> List[dict]:
        """Get available recyclable waste data for buyers."""
        # Get recyclable waste data with user information
        recyclables = db.query(
            WasteData.id,
            WasteData.recyclable_weight,
            WasteData.timestamp,
            User.name.label("user_name"),
            User.email.label("user_email")
        ).join(User).filter(
            WasteData.recyclable_weight > 0
        ).order_by(WasteData.timestamp.desc()).all()
        
        result = []
        for recyclable in recyclables:
            result.append({
                "waste_id": recyclable.id,
                "recyclable_weight": recyclable.recyclable_weight,
                "timestamp": recyclable.timestamp,
                "user_name": recyclable.user_name,
                "user_email": recyclable.user_email
            })
        
        return result
    
    @staticmethod
    def get_recyclable_stats(db: Session) -> dict:
        """Get recyclable waste statistics."""
        total_recyclable = db.query(func.sum(WasteData.recyclable_weight)).scalar() or 0
        total_entries = db.query(WasteData).filter(WasteData.recyclable_weight > 0).count()
        
        # Get recyclable waste by month
        monthly_data = db.query(
            func.date_trunc('month', WasteData.timestamp).label('month'),
            func.sum(WasteData.recyclable_weight).label('total_weight')
        ).filter(
            WasteData.recyclable_weight > 0
        ).group_by(
            func.date_trunc('month', WasteData.timestamp)
        ).order_by('month').all()
        
        monthly_stats = [
            {
                "month": month.strftime("%Y-%m"),
                "total_weight": float(total_weight)
            }
            for month, total_weight in monthly_data
        ]
        
        return {
            "total_recyclable_weight": float(total_recyclable),
            "total_entries": total_entries,
            "monthly_stats": monthly_stats
        }
