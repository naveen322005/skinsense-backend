from fastapi import APIRouter, Depends, HTTPException
from typing import List
from core.dependencies import get_current_user
from schemas.chat_schema import ChatMessage, ChatResponse, ChatHistoryOut
from models.chat import ChatModel
from database import get_database
from services.chatbot_service import get_chatbot_reply

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    payload: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    db = get_database()
    
    # Save user message
    user_msg_model = ChatModel(
        user_id=str(current_user["_id"]),
        role="user",
        content=payload.message
    )
    await db.chats.insert_one(user_msg_model.model_dump(by_alias=True))
    
    # Run Chatbot Service
    reply = await get_chatbot_reply(payload.message)
    
    # Save AI response
    ai_msg_model = ChatModel(
        user_id=str(current_user["_id"]),
        role="ai",
        content=reply
    )
    await db.chats.insert_one(ai_msg_model.model_dump(by_alias=True))
    
    return ChatResponse(reply=reply)

@router.get("/history", response_model=List[ChatHistoryOut])
async def get_history(current_user: dict = Depends(get_current_user)):
    db = get_database()
    cursor = db.chats.find({"user_id": str(current_user["_id"])}).sort("created_at", 1)
    
    history = []
    async for chat in cursor:
        history.append(ChatHistoryOut(
            id=str(chat["_id"]),
            user_id=chat["user_id"],
            role=chat["role"],
            content=chat["content"],
            created_at=str(chat["created_at"])
        ))
    return history
