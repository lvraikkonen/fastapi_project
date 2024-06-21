import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.models import user as user_model, example as example_model
from app.core.config import get_settings
from app.db.database import get_db
import os

# 设置测试环境变量
os.environ["ENVIRONMENT"] = "testing"
# 获取当前环境的配置
settings = get_settings()
# 创建测试数据库引擎
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
# 创建测试会话
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# 覆盖 get_db 依赖项
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


# 创建数据库表的异步函数
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.create_all)
        await conn.run_sync(example_model.Base.metadata.create_all)


# 删除数据库表的异步函数
async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.drop_all)
        await conn.run_sync(example_model.Base.metadata.drop_all)


@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    await create_tables()
    yield
    await drop_tables()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session
