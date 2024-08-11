from pydantic import BaseModel

class DocumentBase(BaseModel):
    content: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
