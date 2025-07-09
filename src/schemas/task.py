from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    owner_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


class TaskRead(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
