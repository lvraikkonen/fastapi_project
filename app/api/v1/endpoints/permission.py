from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.services.permission import (
    get_permission, get_permissions, create_permission, update_permission, delete_permission, get_permission_by_name
)
from app.utils.authorizations import role_required

router = APIRouter()


@router.get("/", response_model=list[Permission])
async def read_permissions(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    permissions = await get_permissions(db, skip=skip, limit=limit)
    return permissions


@router.post("/", response_model=Permission, dependencies=[Depends(role_required(["admin"]))])
async def create_new_permission(permission: PermissionCreate, db: AsyncSession = Depends(get_db_session)):
    db_permission = await get_permission_by_name(db, permission.name)
    if db_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission already exists",
        )
    return await create_permission(db, permission)


@router.put("/{permission_id}", response_model=Permission, dependencies=[Depends(role_required(["admin"]))])
async def update_existing_permission(permission_id: int, permission: PermissionUpdate, db: AsyncSession = Depends(get_db_session)):
    db_permission = await get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    return await update_permission(db, permission_id, permission)


@router.delete("/{permission_id}", response_model=Permission, dependencies=[Depends(role_required(["admin"]))])
async def delete_existing_permission(permission_id: int, db: AsyncSession = Depends(get_db_session)):
    db_permission = await get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )
    return await delete_permission(db, permission_id)
