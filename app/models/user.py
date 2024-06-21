from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base


# 定义 UserRole 中间表，用于多对多关系
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class User(Base):
    """
    用户模型
    - id: 主键，自动递增
    - username: 用户名，唯一且有索引
    - email: 电子邮件，唯一且有索引
    - hashed_password: 存储哈希后的密码
    - is_active: 用户是否活跃，默认为 True
    - is_superuser: 用户是否为超级用户，默认为 False
    - roles: 用户角色
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 添加长度限制
    email = Column(String(100), unique=True, index=True)  # 添加长度限制
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    roles = relationship('Role', secondary=user_roles, back_populates='users')
