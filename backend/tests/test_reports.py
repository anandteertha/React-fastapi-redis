"""
Tests for report endpoints
"""
import pytest
from datetime import datetime


def test_generate_report(client, auth_headers, db_session):
    """Test generating a daily report"""
    # First create a food and meal to have data for the report
    from app.models.food import Food
    from app.models.meal import Meal, MealFood
    from app.models.user import User
    
    user = db_session.query(User).filter(User.username == "testuser").first()
    
    # Create a food
    food = Food(
        name="Test Food",
        calories_per_100g=100.0,
        protein_per_100g=10.0,
        carbs_per_100g=20.0,
        fats_per_100g=5.0
    )
    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)
    
    # Create a meal
    meal = Meal(
        user_id=user.id,
        meal_type="breakfast",
        meal_date=datetime.now()
    )
    db_session.add(meal)
    db_session.commit()
    db_session.refresh(meal)
    
    # Add food to meal
    meal_food = MealFood(
        meal_id=meal.id,
        food_id=food.id,
        quantity_g=200.0
    )
    db_session.add(meal_food)
    db_session.commit()
    
    # Generate report
    response = client.post(
        "/api/v1/reports/generate",
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert "total_calories" in data
    assert "total_protein" in data
    assert "report_date" in data


def test_get_reports(client, auth_headers):
    """Test getting user reports"""
    response = client.get("/api/v1/reports/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_today_report(client, auth_headers, db_session):
    """Test getting today's report"""
    # First create a food and meal to have data for the report
    from app.models.food import Food
    from app.models.meal import Meal, MealFood
    from app.models.user import User
    
    user = db_session.query(User).filter(User.username == "testuser").first()
    
    # Create a food
    food = Food(
        name="Test Food",
        calories_per_100g=100.0,
        protein_per_100g=10.0,
        carbs_per_100g=20.0,
        fats_per_100g=5.0
    )
    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)
    
    # Create a meal for today
    meal = Meal(
        user_id=user.id,
        meal_type="breakfast",
        meal_date=datetime.now()
    )
    db_session.add(meal)
    db_session.commit()
    db_session.refresh(meal)
    
    # Add food to meal
    meal_food = MealFood(
        meal_id=meal.id,
        food_id=food.id,
        quantity_g=200.0
    )
    db_session.add(meal_food)
    db_session.commit()
    
    # Get today's report
    response = client.get("/api/v1/reports/today", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_calories" in data
    assert "report_date" in data

