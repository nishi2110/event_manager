import pytest
from app.main import app
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_username_validation():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register", json={"username": "invalid_username!", "password": "ValidPass123!"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid username format."}
