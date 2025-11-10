import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.services.user_service import user_service

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_users():
    user_service.users = [
        User(name="Alice", email="alice@example.com", age=30, team="Backend", start_date="2024-01-01"),
        User(name="Bob", email="bob@example.com", age=25, team="Frontend", start_date="2024-02-01"),
        User(name="Charlie", email="charlie@example.com", age=35, team="Backend", start_date="2024-03-01"),
    ]
    yield
    user_service.users = []

def test_read_users_all():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Getting Users Data"
    assert len(data["data"]) == 3

def test_read_users_filtered_team():
    response = client.get("/users/", params={"team": "Backend"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert all(u["team"] == "Backend" for u in data["data"])

def test_read_users_no_users():
    user_service.users = []
    response = client.get("/users/")
    data = response.json()
    assert data["status"] == 422
    assert response["message"] == "No Users Data Available"

def test_refresh_users_route():
    response = client.get("/users/refresh")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["message"] == "Refreshing Users Data"
