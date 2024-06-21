from datetime import datetime
from pydantic import BaseModel, Field


class ExampleBase(BaseModel):
    """
    示例基本信息
    - name: 示例名称
    - description: 示例描述
    """
    name: str = Field(..., min_length=1, max_length=100)  # 添加长度限制
    description: str = Field(..., min_length=1, max_length=255)  # 添加长度限制


class ExampleCreate(ExampleBase):
    """
    用于创建示例时不需要额外的字段
    """
    pass


class ExampleUpdate(ExampleBase):
    """
    用于更新示例时需要提供 id
    - id: 示例 ID
    """
    id: int


class Example(ExampleBase):
    """
    返回给客户端的示例模型
    - id: 示例 ID
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
