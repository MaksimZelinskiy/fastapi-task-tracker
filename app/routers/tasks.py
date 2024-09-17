from fastapi import APIRouter, Depends, HTTPException, status, Query
from starlette.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
from ..schemas import task as schemas_task
from ..schemas import user as schemas_user
from ..models import task as models_task
from ..models import user as models_users
from ..models import activity_log as models_activity_logs
from ..core.auth import get_current_user, check_role
from ..database import database
from ..utils import send_status_update_email
from sqlalchemy import and_, select

router = APIRouter()


@router.post("/tasks", response_model=schemas_task.Task)
async def create_task(task: schemas_task.TaskCreate, current_user: schemas_user.User = Depends(check_role(["1", "2"]))):
    """
    Створення нової задачі.

    Цей ендпоінт дозволяє створити нову задачу з вказанням її назви, опису, статусу, пріоритету та виконавців.
    """

    query = models_task.tasks.insert().values(
        title=task.title,
        description=task.description,
        owner_user_id=current_user.id,
        status=task.status,
        priority=task.priority,
        created_at=datetime.utcnow(),
    )
    last_task_id = await database.execute(query)

    # Додаємо виконавців до задачі
    if task.task_assignees:
        for user_id in task.task_assignees:
            await database.execute(models_task.task_assignees.insert().values(task_id=last_task_id, user_id=user_id))

    response = {
        "id": last_task_id,
        "title": task.title,
        "description": task.description,
        "owner_user_id": current_user.id,
        "status": task.status,
        "priority": task.priority,
        "task_assignees": task.task_assignees,
        "owner_user_id": task.owner_user_id, 
        "created_at": datetime.utcnow().isoformat()
    }

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@router.get("/tasks", response_model=List[schemas_task.Task])
async def get_tasks(
    skip: int = 0, 
    limit: int = 10, 
    status: Optional[str] = Query(None, description="Фільтр за статусом (TODO, In progress, Done)"),
    priority: Optional[str] = Query(None, description="Фільтр за пріоритетом (Low, Medium, High)"),
    current_user: schemas_user.User = Depends(get_current_user)
):    
    filters = [models_task.tasks.c.owner_user_id == current_user.id]
    if status is not None:
        filters.append(models_task.tasks.c.status == status)
    if priority is not None:
        filters.append(models_task.tasks.c.priority == priority)

    # LEFT JOIN між таблицями tasks і task_assignees для фільтрації по виконавцям та власникам в фільтрі
    query = select(models_task.tasks).select_from(
            models_task.tasks.outerjoin(models_task.task_assignees, models_task.tasks.c.id == models_task.task_assignees.c.task_id)
    ).where(and_(*filters)).offset(skip).limit(limit)
    
    tasks = await database.fetch_all(query)
    
    tasks_response = []
    for task in tasks:
        assignees_query = models_task.task_assignees.select().where(models_task.task_assignees.c.task_id == task.id)
        assignees = await database.fetch_all(assignees_query)
        
        assignees_response = [{"user_id": assignee.user_id} for assignee in assignees]

        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "task_assignees": assignees_response,
            "owner_user_id": task.owner_user_id, 
            "created_at": task.created_at.isoformat()
        })
    
    return tasks_response


@router.put("/tasks/{task_id}", response_model=schemas_task.Task)
async def update_task(
    task_id: int, 
    task_update: schemas_task.TaskUpdate, 
    current_user: schemas_user.User = Depends(
        check_role(
            ["1", "2", "3"]
            )
        )
    ):
    """
    Оновлення задачі.
    """
    # Отримуємо поточні дані задачі
    task = await database.fetch_one(models_task.tasks.select().where(models_task.tasks.c.id == task_id))
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Оновлюємо дані задачі
    update_data = task_update.dict(exclude_unset=True)

    # Перевіряємо, чи було змінено статус
    old_status = task.status
    new_status = update_data.get('status')

    # Якщо статус змінено, відправляємо сповіщення відповідальній особі
    if new_status and old_status != new_status:
        
        # Отримуємо email власника задачі
        owner = await database.fetch_one(models_users.users.select().where(models_users.users.c.id == task.owner_user_id))
        
        if owner:
            # Відправляємо лист про зміну статусу
            await send_status_update_email(owner.email, task.title, new_status)
        
        # Записуємо зміну статусу в журнал активності
        await database.execute(models_activity_logs.activity_logs.insert().values(
            task_id=task_id, 
            user_id=current_user.id,
            event_type="status_update",
            description=f"Status changed from {old_status} to {new_status}"
            )
        )


    # Оновлюємо виконавців
    if task_update.task_assignees is not None:
        await database.execute(models_task.task_assignees.delete().where(models_task.task_assignees.c.task_id == task_id))
        for user_id in task_update.task_assignees:
            await database.execute(models_task.task_assignees.insert().values(task_id=task_id, user_id=user_id))
        
        # Записуємо зміну виконавців в журнал активності 
        await database.execute(models_activity_logs.activity_logs.insert().values(
            task_id=task_id, 
            user_id=current_user.id,
            event_type="assignee_update",
            description=f"Assignees updated: {task_update.task_assignees}"
            )
        )
    
    # Видаляємо поле "task_assignees", якщо воно є
    update_data.pop('task_assignees', None)
    
    # Оновлюємо задачу в базі
    await database.execute(models_task.tasks.update().where(models_task.tasks.c.id == task_id).values(update_data))

    # отримуємо оновлена задача
    updated_task = await database.fetch_one(models_task.tasks.select().where(models_task.tasks.c.id == task_id))
    
    # отримуємо оновлених виконавців
    assignees_query = models_task.task_assignees.select().where(models_task.task_assignees.c.task_id == task_id)
    assignees = await database.fetch_all(assignees_query)
    assignees_response = [{"user_id": assignee.user_id} for assignee in assignees]

    return {
        "id": updated_task.id,
        "title": updated_task.title,
        "description": updated_task.description,
        "status": updated_task.status,
        "priority": updated_task.priority,
        "task_assignees": assignees_response,
        "owner_user_id": updated_task.owner_user_id, 
        "created_at": updated_task.created_at.isoformat()
    }


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user: schemas_user.User = Depends(check_role(["1"]))):
    """
    Видалення задачі.
    """

    # отримення задачі по ID
    task = await database.fetch_one(models_task.tasks.select().where(models_task.tasks.c.id == task_id))
    
    # якщо такого ID повертаєм помилку 404
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    # користовуч не є власником повертаєм помилку 403 (він не має доступ до видалення чужої таски)
    if task.owner_user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Task not found")

    # процесс видалення
    await database.execute(models_task.task_assignees.delete().where(models_task.task_assignees.c.task_id == task_id))
    await database.execute(models_task.tasks.delete().where(models_task.tasks.c.id == task_id))

    # успіх видалення
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Task deleted"})
