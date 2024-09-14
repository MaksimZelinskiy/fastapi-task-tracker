from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import user as models_user, roles as models_roles
from ..schemas import user as schemas_user
from ..database import database
from .security import verify_password
import os

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(email: str, password: str):
    
    query = models_user.users.select().where(models_user.users.c.email == email)
    user = await database.fetch_one(query)
    
    if user and verify_password(password, user.hashed_password):
        return user
    
    return False

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    query = models_user.users.select().where(models_user.users.c.email == email)
    user = await database.fetch_one(query)
    
    if user is None:
        raise credentials_exception
    
    return user


# Допоміжна функція для перевірки ролі
def check_role(allowed_roles: List[str]=None):
    def role_dependency(current_user: schemas_user.User = Depends(get_current_user)):
        if allowed_roles != None:
            if str(current_user.role_id) not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have the required permissions."
                )
        return current_user
    return role_dependency

