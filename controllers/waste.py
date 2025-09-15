"""
Waste controller for waste data operations
"""
from fastapi import HTTPException, status
from models.database import WasteData, Device, User, execute_query

class WasteController:
    
    @staticmethod
    def upload_waste_data(device_id: str, user_qr: str, organic: float, recyclable: float, hazardous: float):
        """Upload waste data from scanning devices."""
        # Validate device exists and is active
        device = Device.get_by_device_id(device_id)
        
        if not device or not device['is_active']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found or inactive"
            )
        
        # Find user by QR code
        user_query = "SELECT * FROM users WHERE qr_code = %(qr_code)s"
        user = execute_query(user_query, {'qr_code': user_qr}, fetch='one')
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found. Please check QR code."
            )
        
        # Validate waste weights
        if organic < 0 or recyclable < 0 or hazardous < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Waste weights must be non-negative"
            )
        
        # Create waste data entry
        waste_data = WasteData.create(
            user_id=user['id'],
            device_id=device['id'],
            organic_weight=organic,
            recyclable_weight=recyclable,
            hazardous_weight=hazardous
        )
        
        # Calculate and award points (simple calculation)
        organic_points = int(organic * 2)  # 2 points per kg of organic
        recyclable_points = int(recyclable * 3)  # 3 points per kg of recyclable
        hazardous_points = int(hazardous * 5)  # 5 points per kg of hazardous
        total_points = organic_points + recyclable_points + hazardous_points
        
        if total_points > 0:
            # Add individual reward entries for each waste type
            if organic > 0:
                reward_query = """
                INSERT INTO rewards (user_id, points, waste_type, weight)
                VALUES (%(user_id)s, %(points)s, %(waste_type)s, %(weight)s)
                """
                execute_query(reward_query, {
                    'user_id': user['id'],
                    'points': organic_points,
                    'waste_type': 'organic',
                    'weight': organic
                })
            
            if recyclable > 0:
                execute_query(reward_query, {
                    'user_id': user['id'],
                    'points': recyclable_points,
                    'waste_type': 'recyclable',
                    'weight': recyclable
                })
            
            if hazardous > 0:
                execute_query(reward_query, {
                    'user_id': user['id'],
                    'points': hazardous_points,
                    'waste_type': 'hazardous',
                    'weight': hazardous
                })
            
            # Update user's total rewards
            update_rewards_query = "UPDATE users SET rewards = rewards + %(points)s WHERE id = %(user_id)s"
            execute_query(update_rewards_query, {'points': total_points, 'user_id': user['id']})
        
        return waste_data
    
    @staticmethod
    def get_waste_data_by_id(waste_id: int):
        """Get waste data by ID."""
        query = "SELECT * FROM waste_data WHERE id = %(id)s"
        waste_data = execute_query(query, {'id': waste_id}, fetch='one')
        if not waste_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Waste data not found"
            )
        return waste_data
