"""
Tests for user endpoints
"""
import pytest


def test_get_current_user(client, auth_headers):
    """Test getting current user information"""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data
    assert data["username"] == "testuser"


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

