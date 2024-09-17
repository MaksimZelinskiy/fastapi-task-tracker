from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    task_id: int
    content: str

    class Config:
        orm_mode = True
