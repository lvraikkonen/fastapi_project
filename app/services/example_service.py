from sqlalchemy.orm import Session
from app.db import crud
from app.models.models import ExampleData


def get_example_service(db: Session, example_id: int):
    return crud.get_example(db, example_id)


def create_example_service(db: Session, name: str):
    db_example = crud.get_example_by_name(db, name=name)
    if db_example:
        return db_example
    new_example = ExampleData(name=name)
    return crud.create_example(db, new_example)
