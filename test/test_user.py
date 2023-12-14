import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup_user():
    # Simulasi data pendaftaran baru
    data = {
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123",
        "name": "Test User",
    }

    response = client.post("/api/user", json=data)
    assert response.status_code == 200


def test_signup_user_duplicate_username():
    existing_user_data = {
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123",
        "name": "Existing User",
    }

    client.post("/api/user", json=existing_user_data)

    duplicate_user_data = {
        "username": "testuser",
        "password": "password456",
        "confirm_password": "password456",
        "name": "Duplicate User",
    }

    response = client.post("/api/user", json=duplicate_user_data)

    assert response.status_code == 400

def test_signup_user_password_not_match():
    data = {
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password456",  
        "name": "Test User",
    }

    response = client.post("/api/user", json=data)

    assert response.status_code == 400

