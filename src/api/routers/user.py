from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate, UserRead
from src.db.session import get_session
from src.services.user_service import create_user

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user_in: UserCreate, session: AsyncSession = Depends(get_session)
) -> UserRead:
    user = await create_user(user_in, session)
    return UserRead.model_validate(user)
