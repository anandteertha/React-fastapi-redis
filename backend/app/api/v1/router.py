"""
API v1 router - aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, foods, meals, preferences, goals, reports, recommender

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(preferences.router, prefix="/preferences", tags=["preferences"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(recommender.router, prefix="/recommender", tags=["recommender"])

