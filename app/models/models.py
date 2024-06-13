from sqlalchemy import Column, Integer, String
from app.db.base import Base


class ExampleData(Base):
    __tablename__ = "tbl_example"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
