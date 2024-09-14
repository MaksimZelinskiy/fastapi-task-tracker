from sqlalchemy.orm import Session
from ..models.user import roles

# Перелік ролей
default_roles = [
    {"name": "Admin"},
    {"name": "Manager"},
    {"name": "User"}
]

async def init_roles(db: Session):
    """Ініціалізує ролі в базі даних, якщо вони ще не існують."""
    for role in default_roles:
        existing_role = db.execute(roles.select().where(roles.c.name == role['name'])).fetchone()
        if not existing_role:
            db.execute(roles.insert().values(name=role['name']))
    db.commit()