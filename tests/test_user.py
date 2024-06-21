import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import create_user_sync
from app.init_db import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_user(db_session: AsyncSession):
    user_in = UserCreate(username="testuser", email="test@example.com", password="password")
    user = create_user_sync(db_session, user_in)
    yield user
    db_session.delete(user)
    db_session.commit()


def test_read_users(test_user):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_user(test_user):
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == test_user.username


def test_create_user():
    user_in = {"username": "newuser", "email": "newuser@example.com", "password": "password"}
    response = client.post("/auth/register", json=user_in)
    assert response.status_code == 200
    assert response.json()["username"] == user_in["username"]


def test_update_user(test_user):
    user_in = {"username": "updateduser", "email": "updated@example.com"}
    response = client.put(f"/api/v1/users/{test_user.id}", json=user_in)
    assert response.status_code == 200
    assert response.json()["username"] == user_in["username"]


def test_delete_user(test_user):
    response = client.delete(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["username"] == test_user.username


def test_create_user_not_superadmin():
    user_in = {"username": "newuser", "email": "newuser@example.com", "password": "password"}
    response = client.post("/auth/register", json=user_in)
    assert response.status_code == 403  # Assuming 403 Forbidden for non-superadmin users
