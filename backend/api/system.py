# backend/api/system.py
"""
System Settings API - Admin kontrole
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import database
from api.models import system_settings
from api.auth import get_current_user

router = APIRouter(prefix="/system", tags=["system"])

class SystemSettingsUpdate(BaseModel):
    chat_enabled: Optional[bool] = None
    model_auto_load: Optional[bool] = None
    auto_load_model_name: Optional[str] = None
    max_message_length: Optional[int] = None
    rate_limit_messages: Optional[int] = None
    allow_user_model_selection: Optional[bool] = None
    maintenance_mode: Optional[bool] = None
    enable_dark_web_search: Optional[bool] = None
    uncensored_default: Optional[bool] = None
    enable_torrent_search: Optional[bool] = None
    gpu_layers: Optional[int] = None
    threads: Optional[int] = None
    batch_size: Optional[int] = None
    rope_freq_base: Optional[float] = None
    rope_freq_scale: Optional[float] = None
    admin_override_all: Optional[bool] = None

def require_admin(current_user=Depends(get_current_user)):
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin required")
    return current_user

@router.get("/settings")
async def get_system_settings():
    """Get system settings (public)"""
    try:
        query = system_settings.select()
        settings = await database.fetch_one(query)
        
        if not settings:
            # Create default settings
            insert_query = system_settings.insert().values(
                chat_enabled=True,
                model_auto_load=False,
                max_message_length=4000,
                rate_limit_messages=100,
                allow_user_model_selection=True,
                maintenance_mode=False
            )
            await database.execute(insert_query)
            settings = await database.fetch_one(query)
        
        # Convert to dict properly
        if settings:
            return dict(settings)
        return {}
    except Exception as e:
        print(f"❌ Error in /system/settings: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "chat_enabled": True, "model_auto_load": False}

@router.put("/settings")
async def update_system_settings(
    settings_update: SystemSettingsUpdate,
    current_user=Depends(require_admin)
):
    """Update system settings (admin only)"""
    update_data = {}
    
    # Map all possible fields
    field_mapping = {
        'chat_enabled': settings_update.chat_enabled,
        'model_auto_load': settings_update.model_auto_load,
        'auto_load_model_name': settings_update.auto_load_model_name,
        'max_message_length': settings_update.max_message_length,
        'rate_limit_messages': settings_update.rate_limit_messages,
        'allow_user_model_selection': settings_update.allow_user_model_selection,
        'maintenance_mode': settings_update.maintenance_mode,
        'enable_dark_web_search': settings_update.enable_dark_web_search,
        'uncensored_default': settings_update.uncensored_default,
        'enable_torrent_search': settings_update.enable_torrent_search,
        'gpu_layers': settings_update.gpu_layers,
        'threads': settings_update.threads,
        'batch_size': settings_update.batch_size,
        'rope_freq_base': settings_update.rope_freq_base,
        'rope_freq_scale': settings_update.rope_freq_scale,
        'admin_override_all': settings_update.admin_override_all
    }
    
    # Only add non-None values
    for key, value in field_mapping.items():
        if value is not None:
            update_data[key] = value
    
    if update_data:
        # Get first row
        query = system_settings.select()
        existing = await database.fetch_one(query)
        
        if existing:
            update_query = system_settings.update().where(
                system_settings.c.id == existing["id"]
            ).values(**update_data)
        else:
            update_query = system_settings.insert().values(**update_data)
        
        await database.execute(update_query)
    
    return {"message": "System settings updated", "updated": update_data}

@router.get("/health")
async def get_system_health():
    """Check system health - database, files, services"""
    from pathlib import Path
    import sqlite3
    
    health_status = {
        "database": {"status": "error", "message": "Not checked"},
        "backend": {"status": "ok", "message": "Backend is running"},
        "models_folder": {"status": "error", "message": "Not found"},
        "init_required": False
    }
    
    # Check database
    try:
        db_path = Path("/root/MasterCoderAI/backend/data.db")
        if db_path.exists():
            # Check if database has tables AND users
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            # Check if users table has data
            user_count = 0
            chat_count = 0
            try:
                cursor.execute("SELECT COUNT(*) FROM users")
                user_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM chats")
                chat_count = cursor.fetchone()[0]
            except:
                pass
            
            conn.close()
            
            if len(tables) > 0:
                if user_count > 0:
                    health_status["database"] = {
                        "status": "ok",
                        "message": f"{user_count} users, {chat_count} chats",
                        "tables": [t[0] for t in tables],
                        "user_count": user_count,
                        "chat_count": chat_count
                    }
                else:
                    health_status["database"] = {
                        "status": "error",
                        "message": "NO USERS! Click Initialize!",
                        "tables": [t[0] for t in tables],
                        "user_count": 0
                    }
                    health_status["init_required"] = True
            else:
                health_status["database"] = {
                    "status": "warning",
                    "message": "Database exists but no tables found",
                }
                health_status["init_required"] = True
        else:
            health_status["database"] = {
                "status": "error",
                "message": "Database file not found"
            }
            health_status["init_required"] = True
    except Exception as e:
        health_status["database"] = {
            "status": "error",
            "message": f"Database error: {str(e)}"
        }
        health_status["init_required"] = True
    
    # Check models folders
    try:
        model_directories = [
            Path("/root/MasterCoderAI/modeli"),
            Path("/mnt/12T/models")
        ]
        
        total_models = 0
        available_dirs = []
        
        for model_dir in model_directories:
            if model_dir.exists():
                model_files = list(model_dir.glob("*.gguf"))
                total_models += len(model_files)
                available_dirs.append(f"{model_dir}: {len(model_files)} models")
        
        if total_models > 0:
            health_status["models_folder"] = {
                "status": "ok",
                "message": f"Found {total_models} model(s) in {len(available_dirs)} directories",
                "count": total_models,
                "directories": available_dirs
            }
        else:
            health_status["models_folder"] = {
                "status": "warning",
                "message": f"No models found in {len(model_directories)} directories",
                "directories": [str(d) for d in model_directories]
            }
    except Exception as e:
        health_status["models_folder"] = {
            "status": "error",
            "message": f"Error: {str(e)}"
        }
    
    return health_status

@router.post("/initialize")
async def initialize_database(current_user=Depends(require_admin)):
    """Initialize database - create tables and default users"""
    try:
        from api.init_db import init_database
        import asyncio
        
        # Run initialization
        await init_database()
        
        return {
            "status": "success",
            "message": "Database initialized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization failed: {str(e)}")
