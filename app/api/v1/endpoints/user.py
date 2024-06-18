from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import User, UserUpdate

from app.db.database import get_db
from app.services.user import get_user, get_users, update_user, delete_user

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_user = await get_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=User)
async def update_existing_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_user = await update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", response_model=User)
async def delete_existing_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_user = await delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user
