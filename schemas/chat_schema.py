from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class ChatHistoryOut(BaseModel):
    id: str
    user_id: str
    role: str
    content: str
    created_at: str

    class Config:
        from_attributes = True
