"""
Tests for meal endpoints
"""
import pytest
from datetime import datetime


def test_create_meal(client, auth_headers):
    """Test creating a meal"""
    # First create a food
    food_response = client.post(
        "/api/v1/foods/",
        json={
            "name": "Test Food",
            "calories_per_100g": 100.0,
            "protein_per_100g": 10.0,
            "carbs_per_100g": 20.0,
            "fats_per_100g": 5.0
        },
        headers=auth_headers
    )
    food_id = food_response.json()["id"]
    
    # Then create a meal
    response = client.post(
        "/api/v1/meals/",
        json={
            "meal_type": "breakfast",
            "meal_date": datetime.now().isoformat(),
            "foods": [
                {
                    "food_id": food_id,
                    "quantity_g": 200.0
                }
            ]
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["meal_type"] == "breakfast"
    assert len(data["meal_foods"]) == 1
    assert data["total_calories"] > 0


def test_get_meals(client, auth_headers):
    """Test getting user meals"""
    response = client.get("/api/v1/meals/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

