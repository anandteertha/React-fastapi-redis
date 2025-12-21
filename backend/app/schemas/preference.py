"""
Preference schemas for API validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DietaryRestrictionCreate(BaseModel):
    """Schema for creating dietary restriction"""
    restriction_type: str
    severity: str = "moderate"


class PreferenceCreate(BaseModel):
    """Schema for creating user preferences"""
    target_calories: Optional[float] = None
    target_protein: Optional[float] = None
    target_carbs: Optional[float] = None
    target_fats: Optional[float] = None
    preferred_meal_times: Optional[str] = None
    dietary_restrictions: Optional[List[DietaryRestrictionCreate]] = None


class DietaryRestrictionResponse(BaseModel):
    """Schema for dietary restriction response"""
    id: int
    restriction_type: str
    severity: str
    
    class Config:
        from_attributes = True


class PreferenceResponse(BaseModel):
    """Schema for preference response"""
    id: int
    target_calories: Optional[float]
    target_protein: Optional[float]
    target_carbs: Optional[float]
    target_fats: Optional[float]
    preferred_meal_times: Optional[str]
    dietary_restrictions: List[DietaryRestrictionResponse]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

