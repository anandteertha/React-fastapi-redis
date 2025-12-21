"""
Tests for preference endpoints
"""
import pytest


def test_create_preferences(client, auth_headers):
    """Test creating user preferences"""
    response = client.post(
        "/api/v1/preferences/",
        json={
            "target_calories": 2000.0,
            "target_protein": 150.0,
            "target_carbs": 200.0,
            "target_fats": 65.0,
            "dietary_restrictions": [
                {
                    "restriction_type": "vegetarian",
                    "severity": "moderate"
                }
            ]
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["target_calories"] == 2000.0
    assert len(data["dietary_restrictions"]) == 1


def test_get_preferences(client, auth_headers):
    """Test getting user preferences"""
    # First create preferences
    client.post(
        "/api/v1/preferences/",
        json={
            "target_calories": 2000.0,
            "target_protein": 150.0
        },
        headers=auth_headers
    )
    
    # Then get them
    response = client.get("/api/v1/preferences/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["target_calories"] == 2000.0

