"""
Tests for food endpoints
"""
import pytest


def test_create_food(client, auth_headers):
    """Test creating a food item"""
    response = client.post(
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
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Food"
    assert data["calories_per_100g"] == 100.0


def test_get_foods(client, auth_headers):
    """Test getting all foods"""
    response = client.get("/api/v1/foods/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_foods(client, auth_headers):
    """Test searching foods"""
    # First create a food
    client.post(
        "/api/v1/foods/",
        json={
            "name": "Chicken Breast",
            "calories_per_100g": 165.0,
            "protein_per_100g": 31.0,
            "carbs_per_100g": 0.0,
            "fats_per_100g": 3.6
        },
        headers=auth_headers
    )
    
    # Then search
    response = client.get(
        "/api/v1/foods/search?q=chicken",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "chicken" in data[0]["name"].lower()

