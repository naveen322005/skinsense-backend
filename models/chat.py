from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from models.user import PyObjectId

class ChatModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    role: str # 'user' or 'ai'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
