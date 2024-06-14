from sqlalchemy.orm import Session
from app.models.models import User, ExampleData
from app.models.models import UserCreate, ExampleDataCreate
from app.core.security import get_password_hash


def create_example(db: Session, example_data: ExampleDataCreate):
    db_example_data = ExampleData(name=example_data.name, description=example_data.description)
    db.add(db_example_data)
    db.commit()
    db.refresh(db_example_data)
    return db_example_data


def get_example(db: Session, example_id: int):
    return db.query(ExampleData).filter(ExampleData.id == example_id).first()


def get_example_by_name(db: Session, name: str):
    return db.query(ExampleData).filter(ExampleData.name == name).first()


def get_examples(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ExampleData).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
