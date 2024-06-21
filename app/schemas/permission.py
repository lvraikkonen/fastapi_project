from pydantic import BaseModel
from typing import Optional


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class Permission(PermissionInDBBase):
    pass


class PermissionInDB(PermissionInDBBase):
    pass
