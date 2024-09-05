from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    user_id: int