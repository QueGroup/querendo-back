import httpx
import pytest

from . import BASE_URL


# Test for /api/auth/jwt/create/
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"username": "root", "password": "1234"},
        {"username": "root@root.com", "password": "1234"},
        {"username": "+79999999999", "password": "1234"},
    ],
)
async def test_jwt_create_with_username(data):
    url = f"{BASE_URL}/api/auth/jwt/create/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()


# Test for /api/users/telegram-auth/
@pytest.mark.asyncio
async def test_jwt_create_with_telegram_id():
    url = f"{BASE_URL}/api/users/telegram-auth/"
    data = {
        "username": "root",
        "telegram_id": 92233720,
        "password": "1234"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()
