from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..database import metadata

comments = Table(
    'comments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('task_id', Integer, ForeignKey('tasks.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='SET NULL')),
    Column('content', String, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow),
)

