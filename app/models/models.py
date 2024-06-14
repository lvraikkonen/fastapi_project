from sqlalchemy import Column, Integer, String
from app.db.base import Base
from pydantic import BaseModel, ConfigDict


# SQLAlchemy ORM model
class ExampleData(Base):
    __tablename__ = "example_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


# Pydantic model
# Pydantic model
class ExampleDataBase(BaseModel):
    name: str
    description: str


class ExampleDataCreate(ExampleDataBase):
    pass


class ExampleDataInDBBase(ExampleDataBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ExampleDataResponse(ExampleDataInDBBase):
    pass


class ExampleDataInDB(ExampleDataInDBBase):
    pass


# SQLAlchemy ORM model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# Pydantic models
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
