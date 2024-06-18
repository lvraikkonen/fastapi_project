from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from app.db.base import Base  # 确保所有模型在这里导入
from app.models import user as user_model, example as example_model  # 确保所有模型在这里导入
from app.services.user import create_user_sync, get_user_by_username_sync
from app.schemas.user import UserCreate


settings = get_settings()

# 创建同步数据库引擎
sync_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace("sqlite+aiosqlite", "sqlite"), connect_args={"check_same_thread": False})
# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def init_db():
    """
    同步初始化数据库表
    确保在应用启动时调用，创建所有表并创建超级用户
    """
    with sync_engine.begin() as conn:
        try:
            # 创建所有表
            user_model.Base.metadata.create_all(bind=conn)
            example_model.Base.metadata.create_all(bind=conn)
            # 创建超级用户
            db = SessionLocal()
            username = "admin"
            email = "admin@example.com"
            password = "123456"
            user = get_user_by_username_sync(db, username)
            if not user:
                superuser = UserCreate(username=username, email=email, password=password)
                create_user_sync(db, superuser, is_superuser=True)
        except Exception as e:
            conn.rollback()
            raise e


if __name__ == '__main__':
    init_db()
