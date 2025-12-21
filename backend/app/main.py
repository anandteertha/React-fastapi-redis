"""
NutriBite FastAPI Application
Main entry point for the API server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
# Import models to ensure they're registered with SQLAlchemy
from app.models import User, Food, FoodItem, Meal, MealFood, UserPreference, DietaryRestriction, Goal, DailyReport

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriBite API",
    description="A nutrition tracking and recommendation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to NutriBite API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

