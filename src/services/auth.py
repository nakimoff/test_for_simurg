from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from src.db.session import get_session
from src.models.user import User
from src.services.security import verify_password
from src.services.jwt_token import TokenService
from src.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = TokenService.decode_access_token(token)
    except JWTError:
        raise credentials_exception

    result = await session.execute(select(User).where(User.id == token_data.user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
