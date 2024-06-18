from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    用户基本信息
    - username: 用户名
    - email: 电子邮件
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    创建用户模型
    - password: 密码
    """
    password: str


class UserUpdate(UserBase):
    """
    更新用户模型
    - password: 可选密码字段
    """
    password: Optional[str] = None


class User(UserBase):
    """
    返回给客户端的用户模型
    - id: 用户 ID
    - is_active: 用户是否活跃
    - is_superuser: 用户是否为超级用户
    """
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True
