from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.services.security import verify_password


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
