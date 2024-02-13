from fastapi.testclient import TestClient

from src.main import app
from src.repository import user_repository
from src.schema import token_schema

client = TestClient(app)

def test_login_successful():
    data = {
        "username": "joaquinreyero",
        "password": "rootroot"
    }
    response = client.post("/api/login", json=data)
    token_repository = user_repository.TokenRepository()
    token = token_repository.get(token_schema.Params(user_id="3fdc5964-b0ca-4d95-9777-4411a8ea67a1")).token
    assert response.status_code == 200
    assert response.json() == token

def test_login_unauthorized():
    data = {
        "username": "joaquinreyero",
        "password": "rootroot1"
    }
    response = client.post("/api/login", json=data)
    assert response.status_code == 401

def test_login_user_not_active():
    data = {
        "username": "test_not_active",
        "password": "rootroot"
    }
    response = client.post("/api/login", json=data)
    assert response.status_code == 403

def test_login_user_not_found():
    data = {
        "username": "joaquinreyero1",
        "password": "rootroot"
    }
    response = client.post("/api/login", json=data)
    assert response.status_code == 404
