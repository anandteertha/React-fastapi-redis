"""
Meal models - BCNF normalized
Separated into Meal (meal instances) and MealFood (junction table)
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class MealType(str, enum.Enum):
    """Meal type enumeration"""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class Meal(Base):
    """Meal table - normalized to BCNF"""
    __tablename__ = "meals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(SQLEnum(MealType), nullable=False)
    meal_date = Column(DateTime(timezone=True), nullable=False, index=True)
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="meals")
    meal_foods = relationship("MealFood", back_populates="meal", cascade="all, delete-orphan")


class MealFood(Base):
    """Junction table - Meal to Food relationship - normalized to BCNF"""
    __tablename__ = "meal_foods"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    quantity_g = Column(Numeric(10, 2), nullable=False)
    
    # Relationships
    meal = relationship("Meal", back_populates="meal_foods")
    food = relationship("Food", back_populates="meal_foods")

