"""
Food and meal schemas for API validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FoodCreate(BaseModel):
    """Schema for creating food"""
    name: str
    description: Optional[str] = None
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fats_per_100g: float
    fiber_per_100g: float = 0.0
    sugar_per_100g: float = 0.0
    sodium_per_100g: float = 0.0


class FoodResponse(BaseModel):
    """Schema for food response"""
    id: int
    name: str
    description: Optional[str]
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fats_per_100g: float
    fiber_per_100g: float
    sugar_per_100g: float
    sodium_per_100g: float
    
    class Config:
        from_attributes = True


class MealFoodItem(BaseModel):
    """Schema for meal food item"""
    food_id: int
    quantity_g: float


class MealCreate(BaseModel):
    """Schema for creating meal"""
    meal_type: str
    meal_date: datetime
    notes: Optional[str] = None
    foods: List[MealFoodItem]


class MealFoodResponse(BaseModel):
    """Schema for meal food response"""
    id: int
    food_id: int
    quantity_g: float
    food: FoodResponse
    
    class Config:
        from_attributes = True


class MealResponse(BaseModel):
    """Schema for meal response"""
    id: int
    meal_type: str
    meal_date: datetime
    notes: Optional[str]
    meal_foods: List[MealFoodResponse]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    
    class Config:
        from_attributes = True

