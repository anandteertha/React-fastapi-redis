"""
Database models
BCNF-normalized schema
"""
from app.models.user import User
from app.models.food import Food, FoodItem
from app.models.meal import Meal, MealFood
from app.models.preference import UserPreference, DietaryRestriction
from app.models.goal import Goal
from app.models.report import DailyReport

__all__ = [
    "User",
    "Food",
    "FoodItem",
    "Meal",
    "MealFood",
    "UserPreference",
    "DietaryRestriction",
    "Goal",
    "DailyReport"
]

