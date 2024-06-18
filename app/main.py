from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.init_db import init_db
from app.api.v1.endpoints import auth, user, example
from app.core.config import settings
from sqlalchemy import create_engine

from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from app.services.user import create_user_sync, get_user_by_username_sync
from app.schemas.user import UserCreate

# 创建同步引擎
sync_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace("sqlite+aiosqlite", "sqlite"))


# 定义生命周期上下文管理器
@asynccontextmanager
async def lifespan_context(app: FastAPI):
    # 初始化数据库
    init_db()
    yield
    # 在这里可以添加关闭数据库连接等清理操作

# 创建 FastAPI 实例
app = FastAPI(title="My FastAPI Project", version="1.0.0", lifespan=lifespan_context)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根据需要设置允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(example.router, prefix="/api/v1/examples", tags=["examples"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
