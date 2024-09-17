from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import user as schemas_user
from ..schemas import activity_log as schemas_activity_log
from ..models import activity_log as models_activity_log
from ..core.auth import get_current_user, check_role
from ..database import database
from sqlalchemy import and_, select

router = APIRouter()

# Отримання журналу історії активності для задачі
@router.get("/tasks/{task_id}/activity_log", response_model=list[schemas_activity_log.ActivityLog])
async def get_task_activity_log(
    task_id: int,
    current_user: schemas_user.User = Depends(get_current_user)
):
    # Отримуємо журнал активності для конкретної задачі
    query = select(models_activity_log).where(models_activity_log.c.task_id == task_id)
    result = await database.execute(query)
    activity_log = result.fetchall()

    if not activity_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No activity found for this task")

    return activity_log
