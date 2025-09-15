"""
Buyer routes for waste buyers
"""
from fastapi import APIRouter, Depends

from controllers.buyer import BuyerController
from middlewares.auth import get_buyer_user

router = APIRouter(prefix="/buyer", tags=["♻️ Waste Buyers"])

@router.get("/recyclables")
def get_available_recyclables(current_user = Depends(get_buyer_user)):
    """Get available recyclable waste data for buyers."""
    return BuyerController.get_available_recyclables()

@router.get("/stats")
def get_recyclable_stats(current_user = Depends(get_buyer_user)):
    """Get recyclable waste statistics."""
    return BuyerController.get_recyclable_stats()
