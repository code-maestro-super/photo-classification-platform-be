import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "services" / "user-service"))

from fastapi.testclient import TestClient
from app.main import app as user_app


@pytest.fixture
def user_client():
    return TestClient(user_app)


def test_complete_user_flow(user_client):
    email = "flowtest@example.com"
    password = "password123"
    
    register_response = user_client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password}
    )
    assert register_response.status_code == 201
    
    login_response = user_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    me_response = user_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == email

