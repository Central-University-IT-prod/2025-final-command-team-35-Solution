import pytest
import requests


BASE_URL = "https://api.example.com"

@pytest.fixture
def test_user():
    user_data = {"username": "testuser", "password": "testpass"}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 201
    return response.json()
