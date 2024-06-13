from sqlalchemy.orm import Session
from app.models.models import ExampleData, User


def get_example(db: Session, example_id: int):
    return db.query(ExampleData).filter(ExampleData.id == example_id).first()


def get_example_by_name(db: Session, name: str):
    return db.query(ExampleData).filter(ExampleData.name == name).first()


def get_examples(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ExampleData).offset(skip).limit(limit).all()


def create_example(db: Session, example: ExampleData):
    db.add(example)
    db.commit()
    db.refresh(example)
    return example


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
