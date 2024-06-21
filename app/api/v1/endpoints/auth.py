from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.models.user import User as UserInDB
from app.core.config import settings
from app.services.auth import authenticate_user
from app.services.user import create_user, get_user_by_username, get_user_by_email
from app.core.security import create_access_token
from app.api.dependencies import get_db_session, get_active_user

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    # 检查用户名是否已经存在
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # 检查邮箱是否已经存在
    existing_email = await get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user = await create_user(db, user)
    return db_user


@router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_active_user)):
    return current_user
