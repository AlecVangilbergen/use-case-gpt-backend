from pydantic import BaseModel
from typing import Optional, List

class DocumentBase(BaseModel):
    content: str

    class Config:
        orm_mode = True  # This allows the model to work seamlessly with SQLAlchemy


class DocumentCreate(BaseModel):
    content: str
    user_id: Optional[int]  # Optional if user_id is set by the backend

    class Config:
        orm_mode = True

class Document(DocumentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class DocumentSchema(BaseModel):
    content: str
    user_id: Optional[int]  # Optional if user_id is set by the backend

    class Config:
        orm_mode = True

class DocumentOut(BaseModel):
    id: int
    user_id: int
    content: str

    class Config:
        orm_mode = True
