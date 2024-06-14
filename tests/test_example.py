import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.core.config import settings

# 获取测试数据库连接信息
DATABASE_URL = settings.TESTING_DATABASE_URL

# 创建测试数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 FastAPI 测试客户端
client = TestClient(app)


# 在测试之前设置数据库
def setup_module(module):
    Base.metadata.create_all(bind=engine)


# 在测试之后清理数据库
def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


# 测试用户注册
def test_register():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "123456"}
    )
    logging.info(f"user: testuser have registered successful.")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


# 测试用户登录
def test_login():
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# 测试未授权访问
def test_read_example_unauthorized():
    response = client.get("/api/v1/examples/1")
    assert response.status_code == 401


# 测试创建示例
def test_create_example():
    # 登录获取访问令牌
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # 使用访问令牌创建示例
    response = client.post(
        "/api/v1/examples/",
        json={"name": "example1", "description": "sample description"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "example1"


# 测试读取示例
def test_read_example():
    # 登录获取访问令牌
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "123456"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # 使用访问令牌读取示例
    response = client.get(
        "/api/v1/examples/1",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "example1"
