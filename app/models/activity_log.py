from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..database import metadata

activity_logs = Table(
    'activity_log',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL')),
    Column('event_type', String, nullable=False),  # 'status_update', 'assignee_add'
    Column('description', String, nullable=False),  # Опис змін
    Column('created_at', DateTime, default=datetime.utcnow),
)

