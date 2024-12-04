
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user_model import User

client = TestClient(app)

@pytest.mark.asyncio
async def test_username_special_characters(async_client, db_session):
    response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "nickname": "user@name#123",  # Invalid special characters
            "password": "ValidPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 422
    assert "nickname" in response.json()["detail"][0]["loc"]

@pytest.mark.asyncio
async def test_username_length_constraints(async_client, db_session):
    # Test too short
    response = await async_client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "nickname": "a",  # Too short
            "password": "ValidPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 422

    # Test too long
    response = await async_client.post(
        "/users/",
        json={
            "email": "test2@example.com",
            "nickname": "a" * 51,  # Too long
            "password": "ValidPass123!",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response.status_code == 422