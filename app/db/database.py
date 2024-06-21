from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
import logging

# 创建异步数据库引擎，并配置连接池
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    # pool_size=settings.POOL_SIZE,  # 连接池大小
    # max_overflow=settings.MAX_OVERFLOW,  # 连接池已满时可以额外创建的连接数
    # pool_timeout=settings.POOL_TIMEOUT,  # 获取连接的超时时间（秒）
    # pool_recycle=settings.POOL_RECYCLE  # 连接回收时间（秒）
)
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
            logging.error(f"Database session rollback due to: {e}")
            raise e
        finally:
            await session.close()
