import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.schemas.user import UserCreate
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


def test_get_token(test_user):
    response = client.post("/auth/token", data={"username": test_user.username, "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user(test_user):
    token_response = client.post("/auth/token", data={"username": test_user.username, "password": "password"})
    access_token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == test_user.username
