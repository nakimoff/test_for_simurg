from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    priority: TaskPriority


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    priority: Optional[TaskPriority] = None


class TaskRead(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
