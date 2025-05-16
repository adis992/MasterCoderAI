from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from .auth import get_current_user
from .models import users, tasks, user_settings
from .db import database
import psutil
import GPUtil
from passlib.context import CryptContext
from ..ai_engine.model_loader import ModelLoader
import os
import shutil
import requests
from transformers import AutoModel, AutoTokenizer
from pydantic import BaseModel, validator, ValidationError
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])

# Role-based dependency
def require_admin(current_user=Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# Helper: get or create user settings
async def get_user_settings(user_id):
    query = user_settings.select().where(user_settings.c.user_id == user_id)
    row = await database.fetch_one(query)
    if row:
        return dict(row)
    # Create default settings if not exist
    ins = user_settings.insert().values(user_id=user_id)
    await database.execute(ins)
    row = await database.fetch_one(query)
    return dict(row)

async def update_user_settings(user_id, updates: dict):
    await database.execute(user_settings.update().where(user_settings.c.user_id == user_id).values(**updates))
    return await get_user_settings(user_id)

class UserUpdateModel(BaseModel):
    password: Optional[str] = None
    is_admin: Optional[bool] = None

    @validator('password')
    def password_length(cls, v):
        if v is not None and len(v) < 4:
            raise ValueError('Password too short')
        return v

    @validator('is_admin')
    def is_admin_bool(cls, v):
        if v is not None and not isinstance(v, bool):
            raise ValueError('is_admin must be boolean')
        return v

@router.get("/users")
async def list_users(admin=Depends(require_admin)):
    """List all users (admin only)."""
    query = users.select().with_only_columns(
        users.c.id, users.c.username, users.c.is_admin
    )
    result = await database.fetch_all(query)
    return {"status": "ok", "data": [dict(row) for row in result]}

@router.patch("/users/{user_id}")
async def update_user(user_id: int, data: dict, admin=Depends(require_admin)):
    """Update user password and/or admin role (admin only)."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    errors = {}
    update_vals = {}
    # Validacija i mapiranje
    try:
        user_update = UserUpdateModel(**data)
    except ValidationError as e:
        for err in e.errors():
            errors[err['loc'][0]] = err['msg']
        return {"status": "error", "error": errors}
    if user_update.password is not None:
        update_vals['hashed_password'] = pwd_context.hash(user_update.password)
    if user_update.is_admin is not None:
        update_vals['is_admin'] = user_update.is_admin
    if not update_vals:
        return {"status": "error", "error": {"detail": "No fields to update"}}
    await database.execute(users.update().where(users.c.id == user_id).values(**update_vals))
    return {"status": "updated", "data": {"user_id": user_id}}

@router.get("/tasks")
async def list_tasks(admin=Depends(require_admin)):
    """List all tasks"""
    query = tasks.select()
    return {"status": "ok", "data": await database.fetch_all(query)}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, admin=Depends(require_admin)):
    """Delete a task by ID"""
    await database.execute(tasks.delete().where(tasks.c.id == task_id))
    return {"status": "deleted"}

# Resource monitoring
@router.get("/resources")
async def get_resources(admin=Depends(require_admin)):
    """Get CPU, RAM, and GPU resource usage."""
    cpu_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    virtual_mem = psutil.virtual_memory()
    ram_total = virtual_mem.total
    ram_used = virtual_mem.used
    ram_percent = virtual_mem.percent
    # GPU info
    try:
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
    except Exception:
        gpus = []
    return {
        "status": "ok",
        "data": {
            "cpu_count": cpu_count,
            "cpu_percent": cpu_percent,
            "ram_total": ram_total,
            "ram_used": ram_used,
            "ram_percent": ram_percent,
            "gpus": gpus
        }
    }

# Admin settings
@router.get("/settings")
async def get_settings(current_user=Depends(get_current_user)):
    """Get current user/admin settings from DB."""
    settings = await get_user_settings(current_user["id"])
    return {"status": "ok", "data": settings}

@router.post("/settings")
async def update_settings(new_settings: dict, current_user=Depends(get_current_user)):
    """Update user/admin settings in DB (with validation)."""
    allowed = {"cpu_enabled", "gpu_enabled", "temperature", "max_tokens", "active_model"}
    updates = {}
    errors = {}
    for k, v in new_settings.items():
        if k not in allowed:
            errors[k] = "Not allowed"
            continue
        if k == "temperature":
            try:
                v = float(v)
            except Exception:
                errors[k] = "Temperature must be float"
                continue
            if not (0.0 <= v <= 2.0):
                errors[k] = "Temperature must be between 0.0 and 2.0"
                continue
        if k == "max_tokens":
            try:
                v = int(v)
            except Exception:
                errors[k] = "max_tokens must be int"
                continue
            if not (1 <= v <= 8192):
                errors[k] = "max_tokens must be 1-8192"
                continue
        updates[k] = v
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    settings = await update_user_settings(current_user["id"], updates)
    return {"status": "ok", "data": settings}

@router.get("/active_model")
async def get_active_model(admin=Depends(require_admin)):
    """Get currently active model name."""
    settings = await get_user_settings(admin["id"])
    return {"status": "ok", "data": {"active_model": settings.get("active_model")}}

@router.post("/active_model")
async def set_active_model(payload: dict, admin=Depends(require_admin)):
    """Set the active model by name."""
    model_name = payload.get("model_name")
    if not model_name:
        raise HTTPException(status_code=400, detail="Missing model_name")
    await update_user_settings(admin["id"], {"active_model": model_name})
    return {"status": "ok", "data": {"active_model": model_name}}

@router.get("/models")
async def list_models_and_gpus(admin=Depends(require_admin)):
    """List available models and GPUs from backend/models folder only."""
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
    models_list = []
    if os.path.exists(model_dir):
        for d in os.listdir(model_dir):
            path = os.path.join(model_dir, d)
            if os.path.isdir(path) or (os.path.isfile(path) and d.lower().endswith((".gguf", ".bin", ".pt", ".ckpt", ".onnx", ".pkl", ".safetensors"))):
                models_list.append(d)
    # GPU info
    try:
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
    except Exception:
        gpus = []
    settings = await get_user_settings(admin["id"])
    return {"status": "ok", "models": models_list, "gpus": gpus, "active_model": settings.get("active_model")}

@router.post("/upload_model")
async def upload_model(file: UploadFile = File(...), admin=Depends(require_admin)):
    """Upload a model file to backend/models folder. Creates folder if missing."""
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
    os.makedirs(model_dir, exist_ok=True)
    filename = file.filename
    allowed_ext = (".gguf", ".bin", ".pt", ".ckpt", ".onnx", ".pkl", ".safetensors")
    if not filename.lower().endswith(allowed_ext):
        raise HTTPException(status_code=400, detail=f"File type not allowed: {filename}")
    dest_path = os.path.join(model_dir, filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "ok", "filename": filename}

@router.post("/load_model")
async def load_model(payload: dict, admin=Depends(require_admin)):
    """Load a local model (GGUF, PT, BIN) from backend/models folder by name."""
    model_name = payload.get("model_name")
    if not model_name:
        raise HTTPException(status_code=400, detail="Missing model_name")
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
    loader = ModelLoader(model_dir)
    try:
        _, model = loader.load_model_auto(model_name)
        await update_user_settings(admin["id"], {"active_model": model_name})
        return {"status": "ok", "active_model": model_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))