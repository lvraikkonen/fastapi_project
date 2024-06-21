from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db_session
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.role import Role
from app.services.user import (
    get_user, get_users, create_user, update_user, delete_user,
    get_user_roles, assign_role_to_user, remove_role_from_user, get_user_by_username, get_user_by_email
)
from app.utils.authorizations import role_required


router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=list[User])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db_session)):
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User, dependencies=[Depends(role_required(["admin"]))])
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return await create_user(db, user)


@router.put("/{user_id}", response_model=User, dependencies=[Depends(role_required(["admin"]))])
async def update_existing_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return await update_user(db, user_id, user)


@router.delete("/{user_id}", response_model=User, dependencies=[Depends(role_required(["admin"]))])
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found",
        )
    return await delete_user(db, user_id)


@router.get("/{user_id}/roles", response_model=list[Role], dependencies=[Depends(role_required(["admin"]))])
async def read_user_roles(user_id: int, db: AsyncSession = Depends(get_db_session)):
    roles = await get_user_roles(db, user_id)
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roles not found for user",
        )
    return roles


@router.post("/{user_id}/roles/{role_id}", response_model=User, dependencies=[Depends(role_required(["admin"]))])
async def assign_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await assign_role_to_user(db, user_id, role_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Role not found",
        )
    return user


@router.delete("/{user_id}/roles/{role_id}", response_model=User, dependencies=[Depends(role_required(["admin"]))])
async def remove_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await remove_role_from_user(db, user_id, role_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User or Role not found",
        )
    return user
