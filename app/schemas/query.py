from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    查询请求模型
    - query: 查询字符串
    """
    query: str = Field(..., min_length=1)  # 添加长度限制


class QueryResponse(BaseModel):
    """
    查询响应模型
    - result: 查询结果字符串
    """
    result: str = Field(..., min_length=1)  # 添加长度限制
