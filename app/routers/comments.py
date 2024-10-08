from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import user as schemas_user
from ..schemas import comment as schemas_comment
from ..models import task as models_task
from ..models import comment as models_comment
from ..core.auth import get_current_user
from ..database import database
from sqlalchemy import and_, select

router = APIRouter()

# Додавання коментаря до задачі
@router.post("/tasks/{task_id}/comments", response_model=schemas_comment.Comment)
async def add_comment_to_task(
    task_id: int, 
    comment_data: schemas_comment.CommentCreate,
    current_user: schemas_user.User = Depends(get_current_user)
):
    # Перевіряємо, чи існує задача
    task_query = select(models_task.tasks).where(models_task.tasks.c.id == task_id)
    task = await database.execute(task_query)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    last_record_id = await database.execute(
        models_comment.comments.insert().values(
            task_id=task_id,
            user_id=current_user.id,
            content=comment_data.content
        )
    )

    return {**comment_data.dict(), "id": last_record_id, "task_id": task_id}


# Отримання коментарів до задачі
@router.get("/tasks/{task_id}/comments", response_model=list[schemas_comment.Comment])
async def get_comments_for_task(
    task_id: int, 
    current_user: schemas_user.User = Depends(get_current_user)
):
    # Перевіряємо, чи існує задача
    task_query = select(models_task.tasks).where(models_task.tasks.c.id == task_id)
    task = await database.execute(task_query)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Отримуємо коментарі до задачі
    query = select(models_comment.comments).where(models_comment.comments.c.task_id == task_id)
    result = await database.fetch_all(query)

    return result
