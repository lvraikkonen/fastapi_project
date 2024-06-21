from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.core.security import get_password_hash
from app.db.base import Base
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

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
    # 创建所有表
    Base.metadata.create_all(bind=sync_engine)

    # 使用同步会话
    db = SessionLocal()
    try:
        # 检查是否已经存在超级管理员用户
        admin_user = db.query(User).filter(User.username == 'admin').first()
        if admin_user:
            logger.info("Admin user already exists. Skipping initialization.")
            return

        # 创建角色
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.add(admin_role)
        db.add(user_role)
        db.commit()
        db.refresh(admin_role)
        db.refresh(user_role)

        # 创建权限
        read_permission = Permission(name='read')
        write_permission = Permission(name='write')
        delete_permission = Permission(name='delete')
        db.add(read_permission)
        db.add(write_permission)
        db.add(delete_permission)
        db.commit()
        db.refresh(read_permission)
        db.refresh(write_permission)
        db.refresh(delete_permission)

        # 创建超级管理员用户
        admin_user = User(
            username='admin',
            email='admin@example.com',
            hashed_password=get_password_hash('123456'),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # 添加调试信息
        logger.info(f"Admin User: {admin_user}")
        logger.info(f"Admin Role: {admin_role}")

        # 将角色和权限关联到用户和角色
        try:
            admin_user.roles.append(admin_role)
            admin_role.permissions.extend([read_permission, write_permission, delete_permission])
            db.commit()
            logger.info("Roles and permissions successfully assigned.")
        except Exception as e:
            logger.error(f"Error assigning roles and permissions: {e}")
            db.rollback()  # 回滚事务以防数据不一致

        # 确保所有更改已提交
        db.refresh(admin_user)
        db.refresh(admin_role)
        db.refresh(read_permission)
        db.refresh(write_permission)
        db.refresh(delete_permission)
    finally:
        db.close()


if __name__ == '__main__':
    init_db()
