from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT 访问令牌模型
    - access_token: 访问令牌字符串
    - token_type: 令牌类型，通常为 'bearer'
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    JWT 令牌数据模型
    - username: 用户名，可以为 None
    """
    username: Optional[str] = None
