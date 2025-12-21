"""
Tests for recommender endpoints
"""
import pytest


def test_get_recommendations(client, auth_headers, db_session):
    """Test getting recommendations"""
    # Create some foods for recommendations
    from app.models.food import Food
    
    foods = [
        Food(name="Chicken Breast", calories_per_100g=165.0, protein_per_100g=31.0, carbs_per_100g=0.0, fats_per_100g=3.6),
        Food(name="Salmon", calories_per_100g=208.0, protein_per_100g=20.0, carbs_per_100g=0.0, fats_per_100g=12.0),
        Food(name="Broccoli", calories_per_100g=34.0, protein_per_100g=2.8, carbs_per_100g=7.0, fats_per_100g=0.4),
    ]
    for food in foods:
        db_session.add(food)
    db_session.commit()
    
    # Get recommendations
    response = client.get(
        "/api/v1/recommender/recommendations",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)


def test_get_recommendations_with_filters(client, auth_headers, db_session):
    """Test getting recommendations with filters"""
    # Create some foods for recommendations
    from app.models.food import Food
    
    foods = [
        Food(name="Chicken Breast", calories_per_100g=165.0, protein_per_100g=31.0, carbs_per_100g=0.0, fats_per_100g=3.6),
        Food(name="Broccoli", calories_per_100g=34.0, protein_per_100g=2.8, carbs_per_100g=7.0, fats_per_100g=0.4),
    ]
    for food in foods:
        db_session.add(food)
    db_session.commit()
    
    # Get recommendations with filters
    response = client.get(
        "/api/v1/recommender/recommendations?target_calories=2000&dietary_restrictions=vegetarian",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

