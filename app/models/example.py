from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base


class Example(Base):
    """
    示例模型
    - id: 主键，自动递增
    - name: 示例名称，有索引
    - description: 示例描述，有索引
    - created_at: 创建时间，默认值为当前时间
    - updated_at: 修改时间，默认值为当前时间，在更新时自动更新为当前时间
    """
    __tablename__ = "tbl_examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
