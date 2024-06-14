from sqlalchemy.orm import Session
from app.db import crud
from app.models.models import ExampleData, ExampleDataCreate


def create_example_service(db: Session, example_data: ExampleDataCreate):
    return crud.create_example(db, example_data=example_data)


def get_example_service(db: Session, example_id: int):
    return crud.get_example(db, example_id=example_id)


def get_example_by_name_service(db: Session, name: str):
    return crud.get_example_by_name(db, name=name)


def get_examples_service(db: Session, skip: int = 0, limit: int = 10):
    return crud.get_examples(db=db, skip=skip, limit=limit)
