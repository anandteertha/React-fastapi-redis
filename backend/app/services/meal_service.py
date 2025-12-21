"""
Meal service - follows SOLID principles
Single Responsibility: Handles meal-related business logic
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.meal import Meal, MealFood, MealType
from app.models.food import Food
from app.schemas.food import MealCreate
from app.core.redis_client import CacheService


class MealService:
    """Service for meal operations"""
    
    @staticmethod
    def create_meal(db: Session, user_id: int, meal_data: MealCreate) -> Meal:
        """Create a new meal with foods"""
        db_meal = Meal(
            user_id=user_id,
            meal_type=MealType(meal_data.meal_type),
            meal_date=meal_data.meal_date,
            notes=meal_data.notes
        )
        db.add(db_meal)
        db.flush()
        
        # Add foods to meal
        for food_item in meal_data.foods:
            meal_food = MealFood(
                meal_id=db_meal.id,
                food_id=food_item.food_id,
                quantity_g=food_item.quantity_g
            )
            db.add(meal_food)
        
        db.commit()
        db.refresh(db_meal)
        CacheService.delete(f"meals:user:{user_id}")
        return db_meal
    
    @staticmethod
    def get_meal_by_id(db: Session, meal_id: int) -> Optional[Meal]:
        """Get meal by ID with foods"""
        return db.query(Meal).filter(Meal.id == meal_id).first()
    
    @staticmethod
    def get_user_meals(
        db: Session,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Meal]:
        """Get user's meals within date range"""
        cache_key = f"meals:user:{user_id}:{start_date}:{end_date}"
        cached_meals = CacheService.get(cache_key)
        if cached_meals:
            meal_ids = [m["id"] for m in cached_meals]
            return db.query(Meal).filter(Meal.id.in_(meal_ids)).all()
        
        query = db.query(Meal).filter(Meal.user_id == user_id)
        
        if start_date:
            query = query.filter(Meal.meal_date >= start_date)
        if end_date:
            query = query.filter(Meal.meal_date <= end_date)
        
        meals = query.order_by(Meal.meal_date.desc()).all()
        
        if meals:
            CacheService.set(
                cache_key,
                [{"id": m.id} for m in meals],
                expire=600
            )
        return meals
    
    @staticmethod
    def calculate_meal_nutrition(meal: Meal) -> dict:
        """Calculate total nutrition for a meal"""
        total_calories = 0.0
        total_protein = 0.0
        total_carbs = 0.0
        total_fats = 0.0
        
        for meal_food in meal.meal_foods:
            food = meal_food.food
            multiplier = meal_food.quantity_g / 100.0
            
            total_calories += food.calories_per_100g * multiplier
            total_protein += food.protein_per_100g * multiplier
            total_carbs += food.carbs_per_100g * multiplier
            total_fats += food.fats_per_100g * multiplier
        
        return {
            "total_calories": round(total_calories, 2),
            "total_protein": round(total_protein, 2),
            "total_carbs": round(total_carbs, 2),
            "total_fats": round(total_fats, 2)
        }

