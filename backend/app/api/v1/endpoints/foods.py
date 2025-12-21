"""
Food endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.schemas.food import FoodCreate, FoodResponse
from app.services.food_service import FoodService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=FoodResponse, status_code=status.HTTP_201_CREATED)
async def create_food(
    food_data: FoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new food item"""
    return FoodService.create_food(db, food_data)


@router.get("/", response_model=List[FoodResponse])
async def get_foods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all foods with pagination"""
    return FoodService.get_all_foods(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[FoodResponse])
async def search_foods(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search foods by name"""
    return FoodService.search_foods(db, q, limit=limit)


@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get food by ID"""
    food = FoodService.get_food_by_id(db, food_id)
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    return food

