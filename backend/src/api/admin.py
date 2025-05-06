from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user
from .models import users, tasks
from .db import database
import psutil
import GPUtil
from passlib.context import CryptContext

router = APIRouter(prefix="/admin", tags=["admin"])

# Role-based dependency
def require_admin(current_user=Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# In-memory settings store
settings_store = {"cpu_enabled": True, "gpu_enabled": []}

@router.get("/users")
async def list_users(admin=Depends(require_admin)):
    query = users.select().with_only_columns([users.c.id, users.c.username, users.c.is_admin])
    return await database.fetch_all(query)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, admin=Depends(require_admin)):
    await database.execute(users.delete().where(users.c.id == user_id))
    return {"status": "deleted"}

@router.patch("/users/{user_id}")
async def update_user(user_id: int, data: dict, admin=Depends(require_admin)):
    # Update password and/or admin role
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    update_vals = {}
    if 'password' in data:
        update_vals['hashed_password'] = pwd_context.hash(data['password'])
    if 'is_admin' in data:
        update_vals['is_admin'] = data['is_admin']
    if not update_vals:
        raise HTTPException(status_code=400, detail="No fields to update")
    await database.execute(users.update().where(users.c.id == user_id).values(**update_vals))
    return {"status": "updated"}

@router.get("/tasks")
async def list_tasks(admin=Depends(require_admin)):
    query = tasks.select()
    return await database.fetch_all(query)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, admin=Depends(require_admin)):
    await database.execute(tasks.delete().where(tasks.c.id == task_id))
    return {"status": "deleted"}

# Resource monitoring
@router.get("/resources")
async def get_resources(admin=Depends(require_admin)):
    # CPU and memory
    cpu_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    virtual_mem = psutil.virtual_memory()
    ram_total = virtual_mem.total
    ram_used = virtual_mem.used
    ram_percent = virtual_mem.percent
    # GPU info
    gpus = []
    for gpu in GPUtil.getGPUs():
        gpus.append({
            "id": gpu.id,
            "name": gpu.name,
            "load": gpu.load * 100,
            "memory_total": gpu.memoryTotal,
            "memory_used": gpu.memoryUsed,
            "memory_free": gpu.memoryFree
        })
    return {
        "cpu_count": cpu_count,
        "cpu_percent": cpu_percent,
        "ram_total": ram_total,
        "ram_used": ram_used,
        "ram_percent": ram_percent,
        "gpus": gpus
    }

# Admin settings
@router.get("/settings")
async def get_settings(admin=Depends(require_admin)):
    return settings_store

@router.post("/settings")
async def update_settings(new_settings: dict, admin=Depends(require_admin)):
    settings_store.update(new_settings)
    return settings_store