"""
Recommender endpoints - RAG-based recommendations
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.services.recommender_service import RecommenderService
from app.models.user import User

router = APIRouter()
recommender_service = RecommenderService()


@router.get("/recommendations")
async def get_recommendations(
    target_calories: Optional[float] = Query(None),
    dietary_restrictions: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized food recommendations using RAG
    """
    restrictions_list = None
    if dietary_restrictions:
        restrictions_list = [r.strip() for r in dietary_restrictions.split(",")]
    
    recommendations = recommender_service.get_recommendations(
        db=db,
        user_id=current_user.id,
        target_calories=target_calories,
        dietary_restrictions=restrictions_list
    )
    
    return {"recommendations": recommendations}

