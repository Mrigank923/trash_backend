"""
Buyer controller for buyer-specific operations
"""
from models.database import execute_query

class BuyerController:
    
    @staticmethod
    def get_available_recyclables():
        """Get available recyclable waste data for buyers."""
        # Get recyclable waste data with user information
        query = """
        SELECT 
            wd.id as waste_id,
            wd.recyclable_weight,
            wd.timestamp,
            u.name as user_name,
            u.email as user_email
        FROM waste_data wd
        JOIN users u ON wd.user_id = u.id
        WHERE wd.recyclable_weight > 0
        ORDER BY wd.timestamp DESC
        """
        
        return execute_query(query, fetch='all')
    
    @staticmethod
    def get_recyclable_stats():
        """Get recyclable waste statistics."""
        # Get total recyclable weight
        total_query = """
        SELECT 
            COALESCE(SUM(recyclable_weight), 0) as total_recyclable,
            COUNT(*) as total_entries
        FROM waste_data 
        WHERE recyclable_weight > 0
        """
        totals = execute_query(total_query, fetch='one')
        
        # Get monthly statistics
        monthly_query = """
        SELECT 
            DATE_TRUNC('month', timestamp) as month,
            SUM(recyclable_weight) as total_weight
        FROM waste_data 
        WHERE recyclable_weight > 0
        GROUP BY DATE_TRUNC('month', timestamp)
        ORDER BY month
        """
        monthly_data = execute_query(monthly_query, fetch='all')
        
        monthly_stats = [
            {
                "month": row['month'].strftime("%Y-%m"),
                "total_weight": float(row['total_weight'])
            }
            for row in monthly_data
        ]
        
        return {
            "total_recyclable_weight": float(totals['total_recyclable']),
            "total_entries": totals['total_entries'],
            "monthly_stats": monthly_stats
        }
