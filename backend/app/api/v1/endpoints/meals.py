"""
Meal endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.schemas.food import MealCreate, MealResponse
from app.services.meal_service import MealService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal_data: MealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new meal"""
    meal = MealService.create_meal(db, current_user.id, meal_data)
    nutrition = MealService.calculate_meal_nutrition(meal)
    
    # Convert to response model
    response = MealResponse(
        id=meal.id,
        meal_type=meal.meal_type.value,
        meal_date=meal.meal_date,
        notes=meal.notes,
        meal_foods=[
            {
                "id": mf.id,
                "food_id": mf.food_id,
                "quantity_g": mf.quantity_g,
                "food": {
                    "id": mf.food.id,
                    "name": mf.food.name,
                    "description": mf.food.description,
                    "calories_per_100g": mf.food.calories_per_100g,
                    "protein_per_100g": mf.food.protein_per_100g,
                    "carbs_per_100g": mf.food.carbs_per_100g,
                    "fats_per_100g": mf.food.fats_per_100g,
                    "fiber_per_100g": mf.food.fiber_per_100g,
                    "sugar_per_100g": mf.food.sugar_per_100g,
                    "sodium_per_100g": mf.food.sodium_per_100g
                }
            }
            for mf in meal.meal_foods
        ],
        **nutrition
    )
    return response


@router.get("/", response_model=List[MealResponse])
async def get_meals(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's meals"""
    meals = MealService.get_user_meals(db, current_user.id, start_date, end_date)
    
    return [
        MealResponse(
            id=meal.id,
            meal_type=meal.meal_type.value,
            meal_date=meal.meal_date,
            notes=meal.notes,
            meal_foods=[
                {
                    "id": mf.id,
                    "food_id": mf.food_id,
                    "quantity_g": mf.quantity_g,
                    "food": {
                        "id": mf.food.id,
                        "name": mf.food.name,
                        "description": mf.food.description,
                        "calories_per_100g": mf.food.calories_per_100g,
                        "protein_per_100g": mf.food.protein_per_100g,
                        "carbs_per_100g": mf.food.carbs_per_100g,
                        "fats_per_100g": mf.food.fats_per_100g,
                        "fiber_per_100g": mf.food.fiber_per_100g,
                        "sugar_per_100g": mf.food.sugar_per_100g,
                        "sodium_per_100g": mf.food.sodium_per_100g
                    }
                }
                for mf in meal.meal_foods
            ],
            **MealService.calculate_meal_nutrition(meal)
        )
        for meal in meals
    ]


@router.get("/{meal_id}", response_model=MealResponse)
async def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get meal by ID"""
    meal = MealService.get_meal_by_id(db, meal_id)
    if not meal or meal.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found"
        )
    
    return MealResponse(
        id=meal.id,
        meal_type=meal.meal_type.value,
        meal_date=meal.meal_date,
        notes=meal.notes,
        meal_foods=[
            {
                "id": mf.id,
                "food_id": mf.food_id,
                "quantity_g": mf.quantity_g,
                "food": {
                    "id": mf.food.id,
                    "name": mf.food.name,
                    "description": mf.food.description,
                    "calories_per_100g": mf.food.calories_per_100g,
                    "protein_per_100g": mf.food.protein_per_100g,
                    "carbs_per_100g": mf.food.carbs_per_100g,
                    "fats_per_100g": mf.food.fats_per_100g,
                    "fiber_per_100g": mf.food.fiber_per_100g,
                    "sugar_per_100g": mf.food.sugar_per_100g,
                    "sodium_per_100g": mf.food.sodium_per_100g
                }
            }
            for mf in meal.meal_foods
        ],
        **MealService.calculate_meal_nutrition(meal)
    )

