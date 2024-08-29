from pydantic import BaseModel

from app.db.base import Base

class UserBase(BaseModel):
    email: str
    is_active: bool


class UserLogin(BaseModel):
    email: str
    password: str

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
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    user_type: str
