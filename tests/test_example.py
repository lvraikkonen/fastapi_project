import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def token(client):
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpassword"},
    )
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]

def test_read_example_unauthorized(client):
    response = client.get("/api/examples/1")
    assert response.status_code == 401

def test_create_example(client, token):
    response = client.post(
        "/api/examples/",
        json={"name": "example1"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "example1"

def test_read_example(client, token):
    response = client.get(
        "/api/examples/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "example1"
