from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.example_service import get_example_service, create_example_service
from app.core.security import get_current_user
from app.models.models import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/examples/{example_id}")
def read_example(example_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_example = get_example_service(db, example_id=example_id)
    if db_example is None:
        raise HTTPException(status_code=404, detail="ExampleData not found")
    return db_example


@router.post("/examples/")
def create_example(name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_example_service(db, name=name)
