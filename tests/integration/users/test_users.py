import httpx
import pytest

from . import BASE_URL


# Test for /api/users/reg/ and /api/users/me/
@pytest.mark.asyncio
async def test_create_retrieve_delete_user():
    url = f"{BASE_URL}/api/users/reg/"
    retrieve_url = f"{BASE_URL}/api/users/me/"
    jwt_url = f"{BASE_URL}/api/auth/jwt/create/"
    delete_url = f"{BASE_URL}/api/users/me/"
    data = {
        "username": "testuser",
        "email": "users@example.com",
        "password": "testpassword"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)

        assert response.status_code == 201
        jwt_response = await client.post(jwt_url, json={
            "username": data["username"],
            "password": data["password"]
        })
        assert jwt_response.status_code == 200
        user_cred = jwt_response.json()
        assert "access" in jwt_response.json()
        assert "refresh" in jwt_response.json()
        headers = {
            "Authorization": f"Bearer {user_cred['access']}"
        }
        retrieve_response = await client.get(retrieve_url, headers=headers)
        assert retrieve_response.status_code == 200
        delete_response = await client.delete(delete_url, headers=headers)
        assert delete_response.status_code == 204

