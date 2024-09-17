from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    task_id: int
    user_id: Optional[int]
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
