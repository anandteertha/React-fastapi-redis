"""
Report schemas for API validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportResponse(BaseModel):
    """Schema for daily report response"""
    id: int
    report_date: datetime
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    total_fiber: float
    total_sugar: float
    total_sodium: float
    analysis: Optional[str]
    recommendations: Optional[str]
    motivation_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

