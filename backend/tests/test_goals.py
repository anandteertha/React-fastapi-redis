"""
Tests for goal endpoints
"""
import pytest
from datetime import datetime, timedelta


def test_create_goal(client, auth_headers):
    """Test creating a goal"""
    target_date = (datetime.now() + timedelta(days=30)).isoformat()
    response = client.post(
        "/api/v1/goals/",
        json={
            "goal_type": "weight_loss",
            "target_weight_kg": 70.0,
            "current_weight_kg": 80.0,
            "target_date": target_date
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["goal_type"] == "weight_loss"
    assert data["target_weight_kg"] == 70.0
    assert data["current_weight_kg"] == 80.0
    assert "id" in data


def test_get_goals(client, auth_headers):
    """Test getting user goals"""
    response = client.get("/api/v1/goals/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_active_goal(client, auth_headers, db_session):
    """Test getting active goal"""
    from app.models.goal import Goal, GoalType
    from app.models.user import User
    
    user = db_session.query(User).filter(User.username == "testuser").first()
    
    # Create an active goal
    goal = Goal(
        user_id=user.id,
        goal_type=GoalType.weight_loss,
        target_weight_kg=70.0,
        current_weight_kg=80.0,
        target_date=datetime.now() + timedelta(days=30),
        is_active=True
    )
    db_session.add(goal)
    db_session.commit()
    
    # Get active goal
    response = client.get("/api/v1/goals/active", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] is True
    assert data["goal_type"] == "weight_loss"


def test_get_active_goal_not_found(client, auth_headers):
    """Test getting active goal when none exists"""
    response = client.get("/api/v1/goals/active", headers=auth_headers)
    assert response.status_code == 404

