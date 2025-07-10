from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token
from src.schemas.user import LoginRequest
from src.schemas.user import UserLogin

from src.db.session import get_session
from src.services.auth_service import register_user, login_user, get_me
from src.services.deps.auth_dependencies import get_current_user
from src.services.user_service import register_user

from src.models.user import User

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserRead)
async def register(
    user_in: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    return await register_user(user_in, session)


@auth_router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Token:
    return await login_user(credentials.email, credentials.password, session)


@auth_router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)) -> UserRead:
    return await get_me(current_user)
