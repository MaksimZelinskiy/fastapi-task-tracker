from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from ..database import metadata

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True)  # Наприклад, Admin, Manager, User
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, nullable=False, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False)  # Зовнішній ключ на таблицю ролей
)

