# backend/api/user.py
"""
User Routes - Chat Interface, Settings, Chat History
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
import json
import logging

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import database
from api.models import chats, user_settings
from api.auth import get_current_user

logger = logging.getLogger(__name__)

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
    # 🆕 NOVE POSTAVKE
    deeplearning_intensity: Optional[float] = None
    deeplearning_context: Optional[float] = None
    deeplearning_memory: Optional[float] = None
    opinion_confidence: Optional[float] = None
    opinion_creativity: Optional[float] = None
    opinion_critical_thinking: Optional[float] = None
    vscode_auto_open: Optional[bool] = None
    vscode_permissions: Optional[str] = None
    auto_web_search: Optional[bool] = None
    web_search_threshold: Optional[float] = None

class ModelConfigUpdate(BaseModel):
    capabilities: Optional[dict] = None
    capability_settings: Optional[dict] = None
    agent_preferences: Optional[dict] = None

# ==================== USER PROFILE ====================
@router.get("/profile")
async def get_user_profile(current_user=Depends(get_current_user)):
    """Get current user profile information"""
    user_id = current_user.get("id")
    username = current_user.get("username")
    is_admin = current_user.get("is_admin", False)
    
    # Get user chat count
    chat_query = chats.select().where(chats.c.user_id == user_id)
    user_chats = await database.fetch_all(chat_query)
    
    return {
        "id": user_id,
        "username": username,
        "is_admin": is_admin,
        "chat_count": len(user_chats),
        "account_type": "Admin" if is_admin else "User",
        "features": {
            "ai_chat": True,
            "model_loading": is_admin,
            "user_management": is_admin,
            "system_settings": is_admin,
            "tasks_automation": is_admin,
            "database_management": is_admin
        }
    }

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
    """Update user settings - svi novi parametri ukljuceni"""
    update_data = {}
    
    # Standardne postavke
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
    if settings.system_prompt is not None:
        update_data["system_prompt"] = settings.system_prompt
    if settings.theme is not None:
        update_data["theme"] = settings.theme
    
    # 🆕 NOVE POSTAVKE - DeepLearning
    if settings.deeplearning_intensity is not None:
        update_data["deeplearning_intensity"] = settings.deeplearning_intensity
    if settings.deeplearning_context is not None:
        update_data["deeplearning_context"] = settings.deeplearning_context
    if settings.deeplearning_memory is not None:
        update_data["deeplearning_memory"] = settings.deeplearning_memory
    
    # 🎭 Opinion Mode
    if settings.opinion_confidence is not None:
        update_data["opinion_confidence"] = settings.opinion_confidence
    if settings.opinion_creativity is not None:
        update_data["opinion_creativity"] = settings.opinion_creativity
    if settings.opinion_critical_thinking is not None:
        update_data["opinion_critical_thinking"] = settings.opinion_critical_thinking
    
    # 💻 VSCode Integration
    if settings.vscode_auto_open is not None:
        update_data["vscode_auto_open"] = settings.vscode_auto_open
    if settings.vscode_permissions is not None:
        update_data["vscode_permissions"] = settings.vscode_permissions
    
    # 🌐 Web Search
    if settings.auto_web_search is not None:
        update_data["auto_web_search"] = settings.auto_web_search
    if settings.web_search_threshold is not None:
        update_data["web_search_threshold"] = settings.web_search_threshold
    
    if update_data:
        query = user_settings.update().where(
            user_settings.c.user_id == current_user["id"]
        ).values(**update_data)
        await database.execute(query)
        
        print(f"✅ Updated settings for user {current_user['id']}: {update_data}")
    
    return {"message": "Settings updated successfully", "updated_fields": list(update_data.keys())}

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
# ==================== MODEL CONFIGURATION ====================
@router.post("/model-config")
async def save_model_config(
    config: ModelConfigUpdate, 
    current_user=Depends(get_current_user)
):
    """
    💾 SAVE MODEL CONFIGURATION
    Saves user's AI model capabilities and settings
    """
    user_id = current_user.get("id")
    
    try:
        # Convert config to JSON strings for database storage
        capabilities_json = json.dumps(config.capabilities or {})
        settings_json = json.dumps(config.capability_settings or {})
        preferences_json = json.dumps(config.agent_preferences or {})
        
        # Check if model config already exists
        query = """
            SELECT id FROM user_model_config WHERE user_id = :user_id
        """
        existing = await database.fetch_one(query, {"user_id": user_id})
        
        if existing:
            # Update existing config
            update_query = """
                UPDATE user_model_config 
                SET capabilities = :capabilities,
                    capability_settings = :settings,
                    agent_preferences = :preferences,
                    updated_at = datetime('now')
                WHERE user_id = :user_id
            """
            await database.execute(update_query, {
                "user_id": user_id,
                "capabilities": capabilities_json,
                "settings": settings_json,
                "preferences": preferences_json
            })
        else:
            # Create new config
            insert_query = """
                INSERT INTO user_model_config 
                (user_id, capabilities, capability_settings, agent_preferences)
                VALUES (:user_id, :capabilities, :settings, :preferences)
            """
            await database.execute(insert_query, {
                "user_id": user_id,
                "capabilities": capabilities_json,
                "settings": settings_json,
                "preferences": preferences_json
            })
        
        return {
            "success": True,
            "message": "Model configuration saved successfully! 🧠✅",
            "config": {
                "capabilities": config.capabilities,
                "capability_settings": config.capability_settings,
                "agent_preferences": config.agent_preferences
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Model config save error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to save model configuration: {str(e)}"
        )

@router.get("/model-config")
async def get_model_config(current_user=Depends(get_current_user)):
    """
    📖 GET MODEL CONFIGURATION
    Retrieves user's AI model capabilities and settings
    """
    user_id = current_user.get("id")
    
    try:
        query = """
            SELECT capabilities, capability_settings, agent_preferences, updated_at
            FROM user_model_config 
            WHERE user_id = :user_id
        """
        config = await database.fetch_one(query, {"user_id": user_id})
        
        if not config:
            # Return default configuration
            return {
                "success": True,
                "config": {
                    "capabilities": {},
                    "capability_settings": {},
                    "agent_preferences": {}
                },
                "message": "Using default configuration"
            }
        
        import json
        return {
            "success": True,
            "config": {
                "capabilities": json.loads(config["capabilities"]) if config["capabilities"] else {},
                "capability_settings": json.loads(config["capability_settings"]) if config["capability_settings"] else {},
                "agent_preferences": json.loads(config["agent_preferences"]) if config["agent_preferences"] else {}
            },
            "last_updated": str(config["updated_at"])
        }
        
    except Exception as e:
        logger.error(f"❌ Model config get error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve model configuration: {str(e)}"
        )
# ==================== CHAT WITH AI ====================
# This will be implemented in ai.py with model loader integration
