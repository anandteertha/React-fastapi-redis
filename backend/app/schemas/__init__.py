"""
Pydantic schemas for request/response validation
"""
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.food import FoodCreate, FoodResponse, MealCreate, MealResponse
from app.schemas.preference import PreferenceCreate, PreferenceResponse
from app.schemas.goal import GoalCreate, GoalResponse
from app.schemas.report import ReportResponse

__all__ = [
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "FoodCreate",
    "FoodResponse",
    "MealCreate",
    "MealResponse",
    "PreferenceCreate",
    "PreferenceResponse",
    "GoalCreate",
    "GoalResponse",
    "ReportResponse"
]

