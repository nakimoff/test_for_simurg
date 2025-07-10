from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from fastapi import HTTPException, status
from sqlalchemy import select

from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from src.models.user import User

VALID_SORT_FIELDS = {"id", "title", "is_done"}


async def create_task(
    task_in: TaskCreate, session: AsyncSession, owner_id: int
) -> Task:
    task = Task(**task_in.model_dump(), owner_id=owner_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(
    session: AsyncSession,
    user: User,
    is_done: bool | None = None,
    sort: str | None = None,
) -> List[Task]:
    query = select(Task).where(Task.owner_id == user.id)

    if is_done is not None:
        query = query.where(Task.is_done == is_done)

    if sort:
        desc_order = sort.startswith("-")
        sort_field = sort.lstrip("-")
        if hasattr(Task, sort_field):
            sort_column = getattr(Task, sort_field)
            query = query.order_by(
                desc(sort_column) if desc_order else asc(sort_column)
            )

    result = await session.execute(query)
    return list(result.scalars().all())


async def get_task(task_id: int, session: AsyncSession) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def update_task(task_id: int, task_in: TaskUpdate, session: AsyncSession) -> Task:
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(task_id: int, session: AsyncSession) -> None:
    task = await session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
