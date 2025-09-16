"""
User controller for user-specific operations
"""
from fastapi import HTTPException, status
from models.database import User, WasteData, execute_query

class UserController:
    
    @staticmethod
    def get_waste_history(user_id: int):
        """Get user's waste upload history."""
        return WasteData.get_by_user(user_id)
    
    @staticmethod
    def get_user_rewards(user_id: int):
        """Get user's total rewards and reward history."""
        user = User.get_by_id(user_id)
        total_rewards = user['rewards']
        
        reward_history_query = """
        SELECT * FROM rewards 
        WHERE user_id = %(user_id)s 
        ORDER BY created_at DESC
        """
        reward_history = execute_query(reward_history_query, {'user_id': user_id}, fetch='all')
        
        return {
            "total_rewards": total_rewards,
            "reward_history": reward_history
        }
    
    @staticmethod
    def get_qr_code(user_id: int):
        """Get user's QR code."""
        user = User.get_by_id(user_id)
        if not user or not user['qr_code']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR code not found for this user"
            )
        
        return {
            "qr_code": user['qr_code'], 
            "user_id": user['id']
        }
    
    @staticmethod
    def get_user_stats(user_id: int):
        """Get user's waste statistics."""
        user = User.get_by_id(user_id)
        
        # Get waste statistics
        stats_query = """
        SELECT 
            COALESCE(SUM(organic_weight), 0) as total_organic,
            COALESCE(SUM(recyclable_weight), 0) as total_recyclable,
            COALESCE(SUM(hazardous_weight), 0) as total_hazardous,
            COUNT(*) as total_entries
        FROM waste_data 
        WHERE user_id = %(user_id)s
        """
        stats = execute_query(stats_query, {'user_id': user_id}, fetch='one')
        
        total_weight = stats['total_organic'] + stats['total_recyclable'] + stats['total_hazardous']
        
        return {
            "total_organic": float(stats['total_organic']),
            "total_recyclable": float(stats['total_recyclable']),
            "total_hazardous": float(stats['total_hazardous']),
            "total_weight": float(total_weight),
            "total_entries": stats['total_entries'],
            "total_rewards": user['rewards']
        }
    
    @staticmethod
    def get_demo_waste_history(user_id: int):
        """Get user's demo waste upload history with totals."""
        history = WasteData.get_demo_by_user(user_id)
        total_organic = sum(item.get('organic_weight', 0) for item in history)
        total_recyclable = sum(item.get('recyclable_weight', 0) for item in history)
        total_hazardous = sum(item.get('hazardous_weight', 0) for item in history)
        return {
            "history": history,
            "total_organic": float(total_organic),
            "total_recyclable": float(total_recyclable),
            "total_hazardous": float(total_hazardous)
        }
