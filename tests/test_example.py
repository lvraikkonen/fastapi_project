import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.schemas.example import ExampleCreate, ExampleUpdate
from app.services.example import create_example, get_example, delete_example
from app.init_db import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
async def test_example(db_session: AsyncSession):
    example_in = ExampleCreate(name="test example", description="this is a test example")
    example = await create_example(db_session, example_in)
    yield example
    await delete_example(db_session, example.id)


def test_read_examples(test_example):
    response = client.get("/api/v1/examples/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_example(test_example):
    response = client.get(f"/api/v1/examples/{test_example.id}")
    assert response.status_code == 200
    assert response.json()["name"] == test_example.name


def test_create_example():
    example_in = {"name": "new example", "description": "this is a new example"}
    response = client.post("/api/v1/examples/", json=example_in)
    assert response.status_code == 200
    assert response.json()["name"] == example_in["name"]


def test_update_example(test_example):
    example_in = {"name": "updated example", "description": "this is an updated example"}
    response = client.put(f"/api/v1/examples/{test_example.id}", json=example_in)
    assert response.status_code == 200
    assert response.json()["name"] == example_in["name"]


def test_delete_example(test_example):
    response = client.delete(f"/api/v1/examples/{test_example.id}")
    assert response.status_code == 200
    assert response.json()["name"] == test_example.name
