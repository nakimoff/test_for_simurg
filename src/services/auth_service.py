from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.models.user import User
from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token
from src.services.jwt_token import TokenService
from src.services.security import verify_password, get_password_hash
from src.services.auth_utils import authenticate_user
from sqlalchemy import select


async def register_user(user_in: UserCreate, session: AsyncSession) -> UserRead:
    result = await session.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


async def login_user(email: str, password: str, session: AsyncSession) -> Token:
    user = await authenticate_user(email, password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = TokenService.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


async def get_me(user: User) -> UserRead:
    return UserRead.model_validate(user)
