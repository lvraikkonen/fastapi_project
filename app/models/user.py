from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base


class User(Base):
    """
    用户模型
    - id: 主键，自动递增
    - username: 用户名，唯一且有索引
    - email: 电子邮件，唯一且有索引
    - hashed_password: 存储哈希后的密码
    - is_active: 用户是否活跃，默认为 True
    - is_superuser: 用户是否为超级用户，默认为 False
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
