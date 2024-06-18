from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


async def get_user(db: AsyncSession, user_id: int):
    """
    根据用户ID获取用户信息
    :param db: 数据库会话
    :param user_id: 用户ID
    :return: 用户对象，如果未找到则返回 None
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    """
    根据用户名获取用户信息
    :param db: 数据库会话
    :param username: 用户名
    :return: 用户对象，如果未找到则返回 None
    """
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    """
    根据电子邮件获取用户信息
    :param db: 数据库会话
    :param email: 电子邮件
    :return: 用户对象，如果未找到则返回 None
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    获取用户列表
    :param db: 数据库会话
    :param skip: 跳过的记录数
    :param limit: 返回的记录数
    :return: 用户列表
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate, is_superuser: bool = False):
    """
    创建新用户
    :param db: 数据库会话
    :param user: 用户创建模型
    :param is_superuser: 是否是超级管理员
    :return: 创建的用户对象
        """
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user: UserUpdate):
    """
    更新用户信息
    :param db: 数据库会话
    :param user_id: 要更新的前用户id
    :param user: 用户更新模型
    :return: 更新后的用户对象
    """
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    db_user.username = user.username
    db_user.email = user.email
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    """
    删除用户
    :param db: 数据库会话
    :param user_id: 要删除的用户id
    :return: 无
    """
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user


# 同步函数
def get_user_by_username_sync(db: Session, username: str):
    """
    根据用户名获取用户信息（同步）
    :param db: 数据库会话
    :param username: 用户名
    :return: 用户对象，如果未找到则返回 None
    """
    return db.query(User).filter(User.username == username).first()


def create_user_sync(db: Session, user: UserCreate, is_superuser: bool = False):
    """
    创建新用户（同步）
    :param db: 数据库会话
    :param user: 用户创建模型
    :param is_superuser: 是否是超级管理员
    :return: 创建的用户对象
    """
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_active=True,
        is_superuser=is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
