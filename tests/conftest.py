import os
import pytest


@pytest.fixture(scope='module')
def test_client():
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)
