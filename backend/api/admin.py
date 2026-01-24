# backend/api/admin.py
"""
Admin Routes - User Management, System Monitoring, Chat History
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os
import psutil

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import database
from api.models import users, chats, user_settings, tasks
from api.auth import get_current_user
from werkzeug.security import generate_password_hash
import psutil

router = APIRouter(prefix="/admin", tags=["admin"])

# ==================== ROLE CHECK ====================
def require_admin(current_user=Depends(get_current_user)):
    """Check if user is admin"""
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

# ==================== MODELS ====================
class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

# ==================== SYSTEM MONITORING ====================
@router.get("/stats")
async def get_system_stats(current_user=Depends(require_admin)):
    """Get real-time system stats (CPU, RAM, GPU, users, chats)"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # RAM usage
        memory = psutil.virtual_memory()
        ram_total = memory.total / (1024 ** 3)  # GB
        ram_used = memory.used / (1024 ** 3)    # GB
        ram_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024 ** 3)
        disk_used = disk.used / (1024 ** 3)
        disk_percent = disk.percent
        
        # GPU info (try to get if available)
        gpu_info = []
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                gpu_info.append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "memory_used": f"{gpu.memoryUsed}MB",
                    "memory_total": f"{gpu.memoryTotal}MB",
                    "memory_percent": round((gpu.memoryUsed / gpu.memoryTotal) * 100, 1),
                    "gpu_percent": gpu.load * 100,
                    "temperature": gpu.temperature
                })
        except:
            gpu_info = [{"status": "No GPU detected or GPUtil not installed"}]
        
        # Database stats
        total_users_query = "SELECT COUNT(*) as count FROM users"
        total_chats_query = "SELECT COUNT(*) as count FROM chats"
        
        total_users = await database.fetch_one(total_users_query)
        total_chats = await database.fetch_one(total_chats_query)
        
        return {
            "cpu_percent": cpu_percent,
            "cpu_cores": cpu_count,
            "memory_total_gb": round(ram_total, 2),
            "memory_used_gb": round(ram_used, 2),
            "memory_percent": ram_percent,
            "disk_total_gb": round(disk_total, 2),
            "disk_used_gb": round(disk_used, 2),
            "disk_percent": disk_percent,
            "total_users": total_users["count"] if total_users else 0,
            "total_chats": total_chats["count"] if total_chats else 0,
            "gpu_info": gpu_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system stats: {str(e)}")

# ==================== USER MANAGEMENT ====================
@router.get("/users")
async def get_all_users(current_user=Depends(require_admin)):
    """Get all users with chat counts"""
    try:
        # Fetch all users
        query = users.select()
        user_list = await database.fetch_all(query)
        
        result = []
        for user in user_list:
            # Get chat count for this user using SQLAlchemy query
            count_query = chats.select().where(chats.c.user_id == user["id"])
            count_result = await database.fetch_all(count_query)
            chat_count = len(count_result)
            
            result.append({
                "id": user["id"],
                "username": user["username"],
                "is_admin": bool(user["is_admin"]),
                "created_at": str(user["created_at"]) if user["created_at"] else None,
                "total_chats": chat_count
            })
        
        return result
    except Exception as e:
        print(f"❌ Error in /admin/users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@router.post("/users")
async def create_user(user: UserCreate, current_user=Depends(require_admin)):
    """Create new user"""
    # Check if username exists
    query = users.select().where(users.c.username == user.username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password
    hashed_pw = generate_password_hash(user.password)
    
    # Insert user
    insert_query = users.insert().values(
        username=user.username,
        hashed_password=hashed_pw,
        is_admin=user.is_admin
    )
    user_id = await database.execute(insert_query)
    
    # Create default settings
    settings_query = user_settings.insert().values(
        user_id=user_id,
        active_model="default",
        temperature=0.7,
        max_tokens=2048
    )
    await database.execute(settings_query)
    
    return {
        "id": user_id,
        "username": user.username,
        "is_admin": user.is_admin,
        "message": "User created successfully"
    }

@router.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, current_user=Depends(require_admin)):
    """Update user"""
    # Check if user exists
    query = users.select().where(users.c.id == user_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare update data
    update_data = {}
    if user_update.username:
        # Check if new username already exists
        username_check = users.select().where(
            (users.c.username == user_update.username) & (users.c.id != user_id)
        )
        if await database.fetch_one(username_check):
            raise HTTPException(status_code=400, detail="Username already exists")
        update_data["username"] = user_update.username
    if user_update.password:
        update_data["hashed_password"] = generate_password_hash(user_update.password)
    if user_update.is_admin is not None:
        update_data["is_admin"] = user_update.is_admin
    
    if update_data:
        update_query = users.update().where(users.c.id == user_id).values(**update_data)
        await database.execute(update_query)
    
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user=Depends(require_admin)):
    """Delete user"""
    # Prevent deleting yourself
    if user_id == current_user["id"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    # Check if user exists
    query = users.select().where(users.c.id == user_id)
    existing = await database.fetch_one(query)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user (CASCADE will delete related data)
    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)
    
    return {"message": "User deleted successfully"}

# ==================== CHAT HISTORY (ALL USERS) ====================
@router.get("/chats")
async def get_all_chats(current_user=Depends(require_admin), limit: int = 100):
    """Get chat history from all users"""
    query = (
        chats.select()
        .order_by(chats.c.timestamp.desc())
        .limit(limit)
    )
    rows = await database.fetch_all(query)
    
    result = []
    for row in rows:
        # Get username
        user_query = users.select().where(users.c.id == row["user_id"])
        user_row = await database.fetch_one(user_query)
        username = user_row["username"] if user_row else "Unknown"
        
        result.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "username": username,
            "message": row["message"],
            "response": row["response"],
            "model_name": row["model_name"],
            "timestamp": str(row["timestamp"])
        })
    
    return result

@router.get("/chats")
async def get_all_chats(current_user=Depends(require_admin)):
    """Get all chats with user info"""
    query = """
        SELECT c.id, c.user_id, c.message, c.response, c.model_name, c.timestamp, u.username
        FROM chats c
        LEFT JOIN users u ON c.user_id = u.id
        ORDER BY c.timestamp DESC
        LIMIT 1000
    """
    rows = await database.fetch_all(query)
    return [
        {
            "id": row["id"],
            "user_id": row["user_id"],
            "username": row["username"],
            "message": row["message"][:100] if row["message"] else "",  # First 100 chars
            "response": row["response"][:100] if row["response"] else "",  # First 100 chars
            "model_name": row["model_name"],
            "timestamp": str(row["timestamp"])
        }
        for row in rows
    ]

@router.delete("/chats/{chat_id}")
async def delete_chat(chat_id: int, current_user=Depends(require_admin)):
    """Delete specific chat"""
    delete_query = chats.delete().where(chats.c.id == chat_id)
    await database.execute(delete_query)
    return {"message": "Chat deleted successfully"}

@router.delete("/chats/user/{user_id}")
async def delete_user_chats(user_id: int, current_user=Depends(require_admin)):
    """Delete all chats from specific user"""
    delete_query = chats.delete().where(chats.c.user_id == user_id)
    await database.execute(delete_query)
    return {"message": f"All chats from user {user_id} deleted successfully"}

@router.delete("/chats/all")
async def delete_all_chats(current_user=Depends(require_admin)):
    """Delete ALL chats from database (ADMIN ONLY)"""
    delete_query = chats.delete()
    result = await database.execute(delete_query)
    return {"message": "All chats deleted from database", "deleted_count": result}
