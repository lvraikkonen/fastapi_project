from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.services.role import (
    get_role, get_role_by_name, get_roles, create_role, update_role, delete_role
)
from app.utils.authorizations import role_required

router = APIRouter()


@router.get("/", response_model=list[Role])
async def read_roles(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    roles = await get_roles(db, skip=skip, limit=limit)
    return roles


@router.post("/", response_model=Role, dependencies=[Depends(role_required(["admin"]))])
async def create_new_role(role: RoleCreate, db: AsyncSession = Depends(get_db_session)):
    db_role = await get_role_by_name(db, role.name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists",
        )
    return await create_role(db, role)


@router.put("/{role_id}", response_model=Role, dependencies=[Depends(role_required(["admin"]))])
async def update_existing_role(role_id: int, role: RoleUpdate, db: AsyncSession = Depends(get_db_session)):
    db_role = await get_role(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return await update_role(db, role_id, role)


@router.delete("/{role_id}", response_model=Role, dependencies=[Depends(role_required(["admin"]))])
async def delete_existing_role(role_id: int, db: AsyncSession = Depends(get_db_session)):
    db_role = await get_role(db, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return await delete_role(db, role_id)
