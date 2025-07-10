from typing import List, Annotated
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.services.deps.auth_dependencies import get_current_user
from src.schemas.task import TaskCreate, TaskRead, TaskUpdate
from src.services import task_service
from src.models.user import User


router = APIRouter()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    task = await task_service.create_task(task_in, session, owner_id=current_user.id)
    return TaskRead.model_validate(task)


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    is_done: Annotated[bool | None, Query()] = None,
    sort: Annotated[str | None, Query()] = None,
) -> List[TaskRead]:
    tasks = await task_service.get_tasks(session, current_user, is_done, sort)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int, session: AsyncSession = Depends(get_session)
) -> TaskRead:
    task = await task_service.get_task(task_id, session)
    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    task = await task_service.update_task(task_id, task_in, session)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    await task_service.delete_task(task_id, session)
