"""
Service layer - follows SOLID principles
"""
from app.services.user_service import UserService
from app.services.food_service import FoodService
from app.services.meal_service import MealService
from app.services.preference_service import PreferenceService
from app.services.recommender_service import RecommenderService
from app.services.report_service import ReportService

__all__ = [
    "UserService",
    "FoodService",
    "MealService",
    "PreferenceService",
    "RecommenderService",
    "ReportService"
]

