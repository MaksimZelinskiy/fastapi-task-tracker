from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class TaskAssignee(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str = Field(..., example="Complete the report", max_length=255)
    description: Optional[str] = Field(None, example="Prepare the financial report for Q2.")
    owner_user_id: int = Field(..., example=1)
    status: Literal['TODO', 'In progress', 'Done'] = Field("TODO", example="TODO")
    priority: Literal['Low', 'Medium', 'High'] = Field("Low", example="High")


class TaskCreate(TaskBase):
    task_assignees: Optional[List[int]] = Field(default=[], example=[2, 3])


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str]
    status: Optional[Literal['TODO', 'In progress', 'Done']]
    priority: Optional[Literal['Low', 'Medium', 'High']]
    task_assignees: Optional[List[int]] = Field(default=[])

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    task_assignees: List[TaskAssignee] = Field(default=[])

    class Config:
        orm_mode = True
