from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


async def get_permission(db: AsyncSession, permission_id: int):
    """
    根据权限ID获取权限信息
    """
    return await db.get(Permission, permission_id)


async def get_permission_by_name(db: AsyncSession, name: str):
    """
    根据权限名称获取权限信息
    """
    result = await db.execute(select(Permission).filter(Permission.name == name))
    return result.scalars().first()


async def get_permissions(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    获取权限列表
    """
    result = await db.execute(select(Permission).offset(skip).limit(limit))
    return result.scalars().all()


async def create_permission(db: AsyncSession, permission_in: PermissionCreate):
    """
    创建新权限
    """
    permission = Permission(name=permission_in.name, description=permission_in.description)
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission


async def update_permission(db: AsyncSession, permission_id: int, permission_in: PermissionUpdate):
    """
    更新权限信息
    """
    permission = await get_permission(db, permission_id)
    if not permission:
        return None
    permission.name = permission_in.name
    permission.description = permission_in.description
    await db.commit()
    await db.refresh(permission)
    return permission


async def delete_permission(db: AsyncSession, permission_id: int):
    """
    删除权限
    """
    permission = await get_permission(db, permission_id)
    if not permission:
        return None
    await db.delete(permission)
    await db.commit()
    return permission
