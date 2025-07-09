from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token
from src.services.security import get_password_hash
from src.services.jwt_token import TokenService
from src.services.auth import authenticate_user, get_current_user
from src.models.user import User
from src.db.session import get_session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(
        email=user_in.email, hashed_password=get_password_hash(user_in.password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@auth_router.post("/login", response_model=Token)
async def login(
    email: str, password: str, session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(email, password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = TokenService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
