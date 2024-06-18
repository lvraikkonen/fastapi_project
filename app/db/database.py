from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base

# 创建异步数据库引擎
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# 创建异步会话
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# 提供数据库会话，用于依赖注入
async def get_db():
    """
    获取数据库会话
    :yield: 异步数据库会话
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
