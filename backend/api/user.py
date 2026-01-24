# backend/api/user.py
"""
User Routes - Chat Interface, Settings, Chat History
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import database
from api.models import chats, user_settings
from api.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

# ==================== MODELS ====================
class ChatMessage(BaseModel):
    message: str

class SettingsUpdate(BaseModel):
    active_model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    repeat_penalty: Optional[float] = None
    system_prompt: Optional[str] = None
    theme: Optional[str] = None

# ==================== USER SETTINGS ====================
@router.get("/settings")
async def get_user_settings(current_user=Depends(get_current_user)):
    """Get current user settings"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user session")
    
    query = user_settings.select().where(user_settings.c.user_id == user_id)
    row = await database.fetch_one(query)
    
    if not row:
        # Create default settings if not exist
        try:
            insert_query = user_settings.insert().values(
                user_id=user_id,
                active_model="default",
                temperature=0.7,
                max_tokens=2048,
                top_p=0.9,
                top_k=40,
                repeat_penalty=1.1
            )
            await database.execute(insert_query)
            row = await database.fetch_one(query)
        except Exception as e:
            # Return defaults if insert fails
            return {
                "user_id": user_id,
                "active_model": "default",
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
    
    return dict(row) if row else {}

@router.put("/settings")
async def update_user_settings(settings: SettingsUpdate, current_user=Depends(get_current_user)):
    """Update user settings"""
    update_data = {}
    if settings.active_model is not None:
        update_data["active_model"] = settings.active_model
    if settings.temperature is not None:
        update_data["temperature"] = settings.temperature
    if settings.max_tokens is not None:
        update_data["max_tokens"] = settings.max_tokens
    if settings.top_p is not None:
        update_data["top_p"] = settings.top_p
    if settings.top_k is not None:
        update_data["top_k"] = settings.top_k
    if settings.repeat_penalty is not None:
        update_data["repeat_penalty"] = settings.repeat_penalty
    
    if update_data:
        query = user_settings.update().where(
            user_settings.c.user_id == current_user["id"]
        ).values(**update_data)
        await database.execute(query)
    
    return {"message": "Settings updated successfully"}

# ==================== CHAT HISTORY (OWN) ====================
@router.get("/chats")
async def get_my_chats(
    current_user=Depends(get_current_user), 
    user_id: Optional[int] = None,
    limit: int = 50
):
    """Get chat history - own chats for regular users, any user for admins"""
    # If user_id is provided and user is admin, fetch that user's chats
    if user_id is not None:
        if not current_user.get("is_admin"):
            raise HTTPException(status_code=403, detail="Admin access required")
        target_user_id = user_id
    else:
        target_user_id = current_user["id"]
    
    query = (
        chats.select()
        .where(chats.c.user_id == target_user_id)
        .order_by(chats.c.timestamp.desc())
        .limit(limit)
    )
    rows = await database.fetch_all(query)
    
    return [
        {
            "id": row["id"],
            "user_message": row["message"],
            "ai_response": row["response"],
            "model_name": row["model_name"],
            "created_at": str(row["timestamp"])
        }
        for row in rows
    ]

@router.delete("/chats/{chat_id}")
async def delete_my_chat(chat_id: int, current_user=Depends(get_current_user)):
    """Delete specific chat (only own chats)"""
    # Check if chat belongs to current user
    query = chats.select().where(
        (chats.c.id == chat_id) & (chats.c.user_id == current_user["id"])
    )
    existing = await database.fetch_one(query)
    
    if not existing:
        raise HTTPException(status_code=404, detail="Chat not found or not owned by you")
    
    delete_query = chats.delete().where(chats.c.id == chat_id)
    await database.execute(delete_query)
    
    return {"message": "Chat deleted successfully"}

@router.delete("/chats")
async def delete_all_my_chats(current_user=Depends(get_current_user)):
    """Delete all chats from current user"""
    delete_query = chats.delete().where(chats.c.user_id == current_user["id"])
    await database.execute(delete_query)
    
    return {"message": "All your chats deleted successfully"}

# ==================== CHAT WITH AI ====================
# This will be implemented in ai.py with model loader integration
