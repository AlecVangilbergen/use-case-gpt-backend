from pydantic import BaseModel

from app.db.base import Base

class UserBase(BaseModel):
    email: str
    prompt: str


class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    email: str
    password: str
    prompt: str

class UserOut(BaseModel):
    id: int
    email: str
    prompt: str


class UserUpdate(UserBase):
    pass

class UserDB(UserBase):
    id: int

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    prompt: str
    is_superuser: bool

    class Config:
        orm_mode = True
        from_attributes=True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    user_type: str
