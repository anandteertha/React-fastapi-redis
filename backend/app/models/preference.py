"""
User preference models - BCNF normalized
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class UserPreference(Base):
    """User preferences table - normalized to BCNF"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    target_calories = Column(Numeric(10, 2))
    target_protein = Column(Numeric(10, 2))
    target_carbs = Column(Numeric(10, 2))
    target_fats = Column(Numeric(10, 2))
    preferred_meal_times = Column(String(500))  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    dietary_restrictions = relationship("DietaryRestriction", back_populates="preference", cascade="all, delete-orphan")


class DietaryRestriction(Base):
    """Dietary restrictions table - normalized to BCNF"""
    __tablename__ = "dietary_restrictions"
    
    id = Column(Integer, primary_key=True, index=True)
    preference_id = Column(Integer, ForeignKey("user_preferences.id"), nullable=False)
    restriction_type = Column(String(100), nullable=False)  # e.g., "vegetarian", "vegan", "gluten-free"
    severity = Column(String(50), default="moderate")  # "strict", "moderate", "flexible"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    preference = relationship("UserPreference", back_populates="dietary_restrictions")

