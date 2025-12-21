"""
Goal schemas for API validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GoalCreate(BaseModel):
    """Schema for creating goal"""
    goal_type: str
    target_weight_kg: Optional[float] = None
    current_weight_kg: Optional[float] = None
    target_date: Optional[datetime] = None


class GoalResponse(BaseModel):
    """Schema for goal response"""
    id: int
    goal_type: str
    target_weight_kg: Optional[float]
    current_weight_kg: Optional[float]
    target_date: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

