"""
Food models - BCNF normalized
Separated into Food (catalog) and FoodItem (user's food entries)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Food(Base):
    """Food catalog table - normalized to BCNF"""
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    calories_per_100g = Column(Numeric(10, 2), nullable=False)
    protein_per_100g = Column(Numeric(10, 2), nullable=False)
    carbs_per_100g = Column(Numeric(10, 2), nullable=False)
    fats_per_100g = Column(Numeric(10, 2), nullable=False)
    fiber_per_100g = Column(Numeric(10, 2), default=0.0)
    sugar_per_100g = Column(Numeric(10, 2), default=0.0)
    sodium_per_100g = Column(Numeric(10, 2), default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    meal_foods = relationship("MealFood", back_populates="food")


class FoodItem(Base):
    """User's food items - allows customization"""
    __tablename__ = "food_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity_g = Column(Numeric(10, 2), nullable=False)
    custom_name = Column(String(255))  # User can rename
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    food = relationship("Food")

