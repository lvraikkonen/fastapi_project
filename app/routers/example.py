from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.example_service import (
    create_example_service,
    get_example_service,
    get_example_by_name_service,
    get_examples_service
)
from app.models.models import ExampleDataCreate, ExampleDataResponse
from app.core.security import get_current_user
from app.models.models import User

router = APIRouter()


@router.post("/examples/", response_model=ExampleDataResponse)
def create_example(
    example_data: ExampleDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_example_service(db=db, example_data=example_data)


@router.get("/examples/{example_id}", response_model=ExampleDataResponse)
def read_example(
    example_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_example = get_example_service(db=db, example_id=example_id)
    if db_example is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return db_example


@router.get("/examples/name/{name}", response_model=ExampleDataResponse)
def read_example_by_name(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_example = get_example_by_name_service(db=db, name=name)
    if db_example is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return db_example


@router.get("/examples/", response_model=List[ExampleDataResponse])
def read_examples(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    examples = get_examples_service(db=db, skip=skip, limit=limit)
    return examples
