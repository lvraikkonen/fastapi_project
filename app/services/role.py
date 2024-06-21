from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.role import Role, role_permissions
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleUpdate


async def get_role(db: AsyncSession, role_id: int):
    """
    根据角色ID获取角色信息
    """
    return await db.get(Role, role_id)


async def get_role_by_name(db: AsyncSession, name: str):
    """
    根据角色名称获取角色信息
    """
    result = await db.execute(select(Role).filter(Role.name == name))
    return result.scalars().first()


async def get_roles(db: AsyncSession, skip: int = 0, limit: int = 10):
    """
    获取角色列表
    """
    result = await db.execute(select(Role).offset(skip).limit(limit))
    return result.scalars().all()


async def create_role(db: AsyncSession, role_in: RoleCreate):
    """
    创建新角色
    """
    role = Role(name=role_in.name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def update_role(db: AsyncSession, role_id: int, role_in: RoleUpdate):
    """
    更新角色信息
    """
    role = await get_role(db, role_id)
    if not role:
        return None
    role.name = role_in.name
    await db.commit()
    await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role_id: int):
    """
    删除角色
    """
    role = await get_role(db, role_id)
    if not role:
        return None
    await db.delete(role)
    await db.commit()
    return role


async def get_role_permissions(db: AsyncSession, role_id: int) -> list[Permission]:
    """
    获取角色的权限列表
    """
    result = await db.execute(
        select(Permission).join(role_permissions).filter(role_permissions.c.role_id == role_id)
    )
    return result.scalars().all()


async def assign_permission_to_role(db: AsyncSession, role_id: int, permission_id: int):
    """
    为角色分配权限
    """
    role = await get_role(db, role_id)
    permission = await db.get(Permission, permission_id)
    if not role or not permission:
        return None
    role.permissions.append(permission)
    await db.commit()
    return role


async def remove_permission_from_role(db: AsyncSession, role_id: int, permission_id: int):
    """
    从角色移除权限
    """
    role = await get_role(db, role_id)
    if not role:
        return None
    permission = await db.get(Permission, permission_id)
    if permission in role.permissions:
        role.permissions.remove(permission)
        await db.commit()
    return role
