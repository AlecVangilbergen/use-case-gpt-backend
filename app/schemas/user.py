from pydantic import BaseModel

from app.db.base import Base

class UserBase(BaseModel):
    email: str
    is_active: bool

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(UserBase):
    pass

class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    email: str
    is_active: bool
    hashed_password: str
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True
