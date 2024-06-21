from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.auth import oauth2_scheme, get_current_user, get_current_active_user
from app.models.user import User as UserInDB
from app.models.role import Role
from app.models.permission import Permission


async def get_db_session() -> AsyncSession:
    """
    获取数据库会话。
    """
    async for session in get_db():
        yield session


async def get_current_user_dependency(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session)
) -> UserInDB:
    """
    获取当前用户，验证用户身份。
    """
    user = await get_current_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user


async def get_active_user(
    current_user: UserInDB = Depends(get_current_user_dependency)
) -> UserInDB:
    """
    获取当前活跃用户，确保用户是活跃状态
    """
    user = await get_current_active_user(current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return user


async def get_user_roles(
    current_user: UserInDB = Depends(get_active_user),
    db: AsyncSession = Depends(get_db_session)
) -> list[Role]:
    """
    获取当前用户的角色，确保用户有分配的角色
    """
    roles = current_user.roles
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have any roles assigned",
        )
    return roles


async def get_user_permissions(
    current_user: UserInDB = Depends(get_active_user),
    db: AsyncSession = Depends(get_db_session)
) -> list[Permission]:
    """
    获取当前用户的权限，确保用户有分配的权限
    """
    roles = await get_user_roles(current_user, db)
    permissions = []
    for role in roles:
        permissions.extend(role.permissions)
    if not permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have any permissions assigned",
        )
    return permissions
