from app.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


@pytest.fixture(scope="function")
def unique_email():
    import uuid
    return f"user_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture(scope="function")
def unique_password():
    import uuid
    return str(uuid.uuid4())


def test_create_user_sucess(unique_email, unique_password):
    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": unique_password,
        "full_name": "Adelio"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email


def test_login_sucess(unique_email, unique_password):
    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": unique_password,
    })
    assert response.status_code == 200
