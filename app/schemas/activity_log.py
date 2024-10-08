from pydantic import BaseModel
from datetime import datetime

class ActivityLog(BaseModel):
    id: int
    task_id: int
    user_id: int
    event_type: str
    description: str

    class Config:
        orm_mode = True
