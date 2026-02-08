"""
MasterCoderAI - Main API
Jednostavan, čist, funkcionalan backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os
from pathlib import Path
from datetime import datetime

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.auth import router as auth_router
from api.admin import router as admin_router
from api.user import router as user_router
from api.ai import router as ai_router
from api.system import router as system_router
from api.tasks import router as tasks_router
from api.integrations import router as integrations_router  # 🟣 VIBER & IPTV
from agents.agents_api import router as agents_router  # 🤖 AGENT SYSTEM
from db.database import database

app = FastAPI(title="MasterCoderAI API", version="2.0.0")

# CORS - dozvoli sve za LAN pristup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database lifecycle
@app.on_event("startup")
async def startup():
    await database.connect()
    print("✅ Database connected")
    
    # Mark database as initialized
    from api.system import SERVER_INITIALIZATION_STATE
    SERVER_INITIALIZATION_STATE["components"]["database"] = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "message": "Database connected"
    }
    
    # AUTO-LOAD MODEL if enabled in settings
    try:
        from api.models import system_settings
        query = system_settings.select()
        settings = await database.fetch_one(query)
        
        if settings and settings.get("model_auto_load") and settings.get("auto_load_model_name"):
            model_name = settings["auto_load_model_name"]
            print(f"🚀 AUTO-LOAD enabled: Loading {model_name}...")
            
            # Import AI module to access model loading
            from api import ai
            from pathlib import Path
            
            model_path = Path(f"/root/MasterCoderAI/modeli/{model_name}")
            if model_path.exists():
                # Mark auto-load as started
                SERVER_INITIALIZATION_STATE["components"]["auto_load"] = {
                    "status": "loading",
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Loading {model_name}..."
                }
                
                # Load model in background
                import asyncio
                asyncio.create_task(ai.auto_load_model_on_startup(model_name))
            else:
                print(f"⚠️ AUTO-LOAD model {model_name} not found!")
                SERVER_INITIALIZATION_STATE["components"]["auto_load"] = {
                    "status": "error",
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Model {model_name} not found"
                }
        else:
            # No auto-load
            SERVER_INITIALIZATION_STATE["components"]["auto_load"] = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "message": "Auto-load disabled"
            }
    except Exception as e:
        print(f"⚠️ AUTO-LOAD error: {e}")
        SERVER_INITIALIZATION_STATE["components"]["auto_load"] = {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "message": f"Auto-load error: {str(e)}"
        }

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    print("✅ Database disconnected")

# Routes
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(ai_router)
app.include_router(system_router)
app.include_router(tasks_router)
app.include_router(integrations_router)  # 🟣 VIBER & IPTV INTEGRATION
app.include_router(agents_router)  # 🤖 BRUTALNI AGENT SYSTEM

@app.get("/api/status")
async def api_status():
    """API endpoint for status - separate from root"""
    import sys
    from pathlib import Path
    
    # Provjeri modele
    model_dir = Path("/root/MasterCoderAI/modeli")
    models = []
    if model_dir.exists():
        models = [f.name for f in model_dir.iterdir() if f.suffix in ['.gguf', '.bin', '.pt']]
    
    # Provjeri bazu
    db_path = Path("/root/MasterCoderAI/backend/data.db")
    db_status = "connected" if db_path.exists() else "not found"
    
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "python_status": "installed",
        "models_found": len(models),
        "models": models,
        "database_status": db_status,
        "system_status": "operational"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}

@app.get("/status")
async def status():
    """System status - provjera modela, Python-a, baze"""
    import sys
    from pathlib import Path
    
    # Provjeri modele
    model_dir = Path("/root/MasterCoderAI/modeli")
    models = []
    if model_dir.exists():
        models = [f.name for f in model_dir.iterdir() if f.suffix in ['.gguf', '.bin', '.pt']]
    
    # Provjeri bazu
    db_path = Path("/root/MasterCoderAI/backend/data.db")
    db_status = "connected" if db_path.exists() else "not found"
    
    return {
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "python_status": "installed",
        "models_found": len(models),
        "models": models,
        "database_status": db_status,
        "system_status": "operational"
    }

@app.get("/admin/models")
async def list_models():
    """Lista svih modela iz modeli/ foldera"""
    from pathlib import Path
    model_dir = Path("/root/MasterCoderAI/modeli")
    models = []
    if model_dir.exists():
        models = [f.name for f in model_dir.iterdir() if f.suffix in ['.gguf', '.bin', '.pt']]
    return {"models": models}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
