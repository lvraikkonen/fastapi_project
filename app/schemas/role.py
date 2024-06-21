from pydantic import BaseModel
from typing import List, Optional


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    permissions: Optional[List[str]] = []


class RoleInDB(RoleInDBBase):
    pass
