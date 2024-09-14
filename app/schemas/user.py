from pydantic import BaseModel, EmailStr 

class UserCreate(BaseModel):
    email: str
    password: str
    username: str


class User(BaseModel):
    id: int
    email: EmailStr  
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
