"""
Buyer routes for waste buyers
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.buyer import BuyerController
from middlewares.auth import require_buyer

router = APIRouter(
    prefix="/buyer", 
    tags=["♻️ Waste Buyers"],
    dependencies=[Depends(require_buyer)],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Buyer access required"},
        404: {"description": "Resource not found"}
    }
)

@router.get(
    "/recyclables",
    summary="Get available recyclable materials",
    description="""
    Retrieve comprehensive data about available recyclable waste materials.
    
    **Recyclable Materials Access:**
    - View all available recyclable waste inventory
    - Access material specifications and quantities
    - Monitor collection locations and timelines
    - Track material quality and processing requirements
    
    **Business Intelligence:**
    - Real-time inventory updates
    - Material categorization and sorting
    - Quality assessment data
    - Collection scheduling information
    
    **Buyer Benefits:**
    - Direct access to waste stream data
    - Quality assured materials
    - Sustainable sourcing verification
    - Competitive pricing opportunities
    
    **Material Categories:**
    - Paper and cardboard
    - Plastics (by type and grade)
    - Metals and electronics
    - Glass and ceramics
    """,
    responses={
        200: {
            "description": "Recyclable materials retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "material_type": "plastic",
                            "total_weight": 150.5,
                            "collection_points": 15,
                            "quality_grade": "A",
                            "availability_date": "2025-09-15T00:00:00",
                            "estimated_value": 225.75
                        }
                    ]
                }
            }
        }
    }
)
def get_available_recyclables(
    current_user = Depends(require_buyer),
    db: Session = Depends(get_db)
):
    """Get available recyclable waste data for buyers."""
    return BuyerController.get_available_recyclables(db)

@router.get(
    "/stats",
    summary="Get recyclable waste statistics",
    description="""
    Access comprehensive statistics and analytics for recyclable waste materials.
    
    **Statistical Analysis:**
    - Historical collection trends
    - Material quality distributions
    - Regional availability patterns
    - Seasonal collection variations
    
    **Market Intelligence:**
    - Material value trends
    - Competition analysis
    - Supply chain optimization
    - Demand forecasting data
    
    **Performance Metrics:**
    - Collection efficiency rates
    - Material processing times
    - Quality consistency measures
    - Environmental impact data
    
    **Strategic Planning:**
    - Long-term availability projections
    - Market opportunity analysis
    - Sustainability impact metrics
    - Cost-benefit assessments
    """,
    responses={
        200: {
            "description": "Recyclable statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_recyclable_weight": 5250.75,
                        "material_breakdown": {
                            "plastic": {"weight": 2100.25, "percentage": 40.0},
                            "paper": {"weight": 1575.50, "percentage": 30.0},
                            "metal": {"weight": 1050.00, "percentage": 20.0},
                            "glass": {"weight": 525.00, "percentage": 10.0}
                        },
                        "monthly_trends": [],
                        "quality_distribution": {
                            "grade_A": 60.5,
                            "grade_B": 35.2,
                            "grade_C": 4.3
                        },
                        "estimated_total_value": 7876.12
                    }
                }
            }
        }
    }
)
def get_recyclable_stats(
    current_user = Depends(require_buyer),
    db: Session = Depends(get_db)
):
    """Get recyclable waste statistics."""
    return BuyerController.get_recyclable_stats(db)
