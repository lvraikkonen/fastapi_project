from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.example import Example, ExampleCreate, ExampleUpdate
from app.models.user import User as UserInDB

from app.db.database import get_db
from app.services.example import create_example, get_example, get_examples, update_example, delete_example
from app.services.auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Example)
async def create_new_example(
    example: ExampleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db_example = await create_example(db, example)
    return db_example


@router.get("/{example_id}", response_model=Example)
async def read_example(
    example_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db_example = await get_example(db, example_id)
    if db_example is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Example not found"
        )
    return db_example


@router.get("/", response_model=List[Example])
async def read_examples(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    examples = await get_examples(db, skip=skip, limit=limit)
    return examples


@router.put("/{example_id}", response_model=Example)
async def update_existing_example(
    example_id: int,
    example: ExampleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db_example = await update_example(db, example_id, example)
    if db_example is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Example not found"
        )
    return db_example


@router.delete("/{example_id}", response_model=Example)
async def delete_existing_example(
    example_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user)
):
    db_example = await delete_example(db, example_id)
    if db_example is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Example not found"
        )
    return db_example
