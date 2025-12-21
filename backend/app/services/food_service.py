"""
Food service - follows SOLID principles
Single Responsibility: Handles food-related business logic
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.food import Food
from app.schemas.food import FoodCreate
from app.core.redis_client import CacheService


class FoodService:
    """Service for food operations"""
    
    @staticmethod
    def create_food(db: Session, food_data: FoodCreate) -> Food:
        """Create a new food item"""
        db_food = Food(**food_data.model_dump())
        db.add(db_food)
        db.commit()
        db.refresh(db_food)
        CacheService.delete("foods:list")
        return db_food
    
    @staticmethod
    def get_food_by_id(db: Session, food_id: int) -> Optional[Food]:
        """Get food by ID"""
        cache_key = f"food:id:{food_id}"
        cached_food = CacheService.get(cache_key)
        if cached_food:
            return db.query(Food).filter(Food.id == food_id).first()
        
        food = db.query(Food).filter(Food.id == food_id).first()
        if food:
            CacheService.set(cache_key, {"id": food.id}, expire=3600)
        return food
    
    @staticmethod
    def search_foods(db: Session, query: str, limit: int = 20) -> List[Food]:
        """Search foods by name"""
        cache_key = f"foods:search:{query}:{limit}"
        cached_foods = CacheService.get(cache_key)
        if cached_foods:
            food_ids = [f["id"] for f in cached_foods]
            return db.query(Food).filter(Food.id.in_(food_ids)).all()
        
        # Case-insensitive search for MySQL
        search_pattern = f"%{query}%"
        foods = db.query(Food).filter(
            Food.name.like(search_pattern)
        ).limit(limit).all()
        
        if foods:
            CacheService.set(
                cache_key,
                [{"id": f.id} for f in foods],
                expire=1800
            )
        return foods
    
    @staticmethod
    def get_all_foods(db: Session, skip: int = 0, limit: int = 100) -> List[Food]:
        """Get all foods with pagination"""
        cache_key = f"foods:list:{skip}:{limit}"
        cached_foods = CacheService.get(cache_key)
        if cached_foods:
            food_ids = [f["id"] for f in cached_foods]
            return db.query(Food).filter(Food.id.in_(food_ids)).all()
        
        foods = db.query(Food).offset(skip).limit(limit).all()
        if foods:
            CacheService.set(
                cache_key,
                [{"id": f.id} for f in foods],
                expire=1800
            )
        return foods

