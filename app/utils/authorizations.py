from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session, get_current_user_dependency, get_active_user
from app.services.auth import get_current_user_roles, get_current_user_permissions
from app.models.user import User as UserInDB
from app.models.role import Role
from app.models.permission import Permission


def role_required(required_roles: list[str]):
    async def role_checker(
        current_user: UserInDB = Depends(get_active_user),
        db: AsyncSession = Depends(get_db_session)
    ):
        roles = await get_current_user_roles(current_user, db)
        user_role_names = [role.name for role in roles]
        if not any(role in user_role_names for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required roles",
            )
    return role_checker


def permission_required(required_permissions: list[str]):
    async def permission_checker(
        current_user: UserInDB = Depends(get_active_user),
        db: AsyncSession = Depends(get_db_session)
    ):
        permissions = await get_current_user_permissions(current_user, db)
        user_permission_names = [permission.name for permission in permissions]
        if not any(permission in user_permission_names for permission in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have the required permissions",
            )
    return permission_checker
