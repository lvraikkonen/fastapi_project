import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


# Choose the database URL based on the environment
environment = os.getenv("FASTAPI_ENV", "dev")

if environment == "production":
    SQLALCHEMY_DATABASE_URL = settings.PRODUCTION_DATABASE_URL
elif environment == "test":
    SQLALCHEMY_DATABASE_URL = settings.TESTING_DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.DEVELOPMENT_DATABASE_URL


# 创建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
