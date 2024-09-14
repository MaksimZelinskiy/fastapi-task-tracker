from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, MetaData, Float
from ..database import metadata
from datetime import datetime

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("description", String),
    Column("owner_user_id", Integer, ForeignKey("users.id")),
    Column("status", String, nullable=False, default="TODO"),  # Можно использовать Enum
    Column("priority", String, nullable=False, default="High"),
    Column("created_at", DateTime, default=datetime.utcnow),
)

task_assignees = Table(
    "task_assignees",
    metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)