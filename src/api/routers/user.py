from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.schemas.user import UserCreate, UserRead
from src.models.user import User
from src.db.session import get_session
from src.services.security import get_password_hash

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_pw)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
