import logging
from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
# Development imports
from .middleware import LoggingMiddleware
# Production middleware (commented out for dev; uncomment in production):
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from .middleware import RateLimitMiddleware
from .ws_endpoints import router as ws_router
from .auth import router as auth_router, get_current_user
from .db import database, engine, metadata
from .models import users, chats
from passlib.context import CryptContext
from .db import DATABASE_URL as DB_URL
from .admin import router as admin_router  # Ispravan lokalni import admin routera
import psutil
import GPUtil

# Configure logging to file
logging.basicConfig(filename="mastercoderai.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")

# Inicijalizacija rate limiter-a
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter  # Register the limiter in app.state for SlowAPI middleware
app.include_router(auth_router)
app.include_router(admin_router)  # Omogući admin API rute
# Logging
app.add_middleware(LoggingMiddleware)
# Production: re-enable for production environment
# app.add_middleware(HTTPSRedirectMiddleware)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["yourdomain.com"])
# app.add_middleware(RateLimitMiddleware)
# Dodavanje SlowAPI middleware-a za integraciju rate limiting-a
app.add_middleware(SlowAPIMiddleware)
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict to localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ws_router)

# Database connect/disconnect and user seeding
@app.on_event("startup")
async def startup():
    # Retry connecting to the database and creating tables
    import asyncio
    from sqlalchemy.exc import OperationalError
    import os, psycopg2
    db_name = DB_URL.rsplit('/', 1)[1]
    default_url = DB_URL.rsplit('/', 1)[0] + "/postgres"
    retries = 5
    for n in range(retries):
        try:
            # Connect and auto-create database if missing
            await database.connect()
            break
        except OperationalError as e:
            if f"database \"{db_name}\" does not exist" in str(e):
                conn = psycopg2.connect(default_url)
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute(f"CREATE DATABASE {db_name}")
                cur.close()
                conn.close()
                logging.info(f"Auto-created database {db_name}")
            logging.info(f"Database not ready (attempt {n+1}/{retries}): {e}")
            await asyncio.sleep(2)
    else:
        logging.error("Could not connect to database after retries")
        raise
    # Create tables after ensuring database exists
    metadata.create_all(engine)
    # Ensure admin and test user exist, always reset admin password to 'admin'
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    for username, password, is_admin in [("admin", "admin", True), ("user", "user", False)]:
        query = users.select().where(users.c.username == username)
        existing = await database.fetch_one(query)
        hashed = pwd.hash(password)
        if not existing:
            await database.execute(users.insert().values(
                username=username, hashed_password=hashed, is_admin=is_admin
            ))
        elif username == "admin":
            # Always reset admin password to 'admin' for testing
            await database.execute(users.update().where(users.c.username == "admin").values(hashed_password=hashed))

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    # Bypass authentication: default user_id 1
    resp_text = f"Echo: {message}"
    await database.execute(chats.insert().values(
        user_id=1, message=message, response=resp_text
    ))
    return {"response": resp_text}

@app.get("/chats")
async def get_chats():
    # Bypass authentication: default user_id 1
    query = chats.select().where(chats.c.user_id == 1).order_by(chats.c.timestamp)
    results = await database.fetch_all(query)
    return [{"id": r['id'], "message": r['message'], "response": r['response'], "timestamp": r['timestamp'].isoformat()} for r in results]

@app.get("/limited")
@limiter.limit("10/minute")
async def limited_endpoint(request: Request):
    return {"message": "Ovaj endpoint je ograničen na 10 zahtjeva po minuti."}

@app.get("/secure-endpoint")
async def secure_endpoint():
    return {"message": "Ovo je siguran endpoint sa svim implementiranim mjerama."}

@app.get("/system-info")
async def get_system_info():
    # Get CPU information
    cpu_count = psutil.cpu_count(logical=True)
    cpu_cores = psutil.cpu_count(logical=False)

    # Get GPU information
    gpus = []
    for gpu in GPUtil.getGPUs():
        gpus.append({
            "id": gpu.id,
            "name": gpu.name,
            "total_memory": gpu.memoryTotal,
            "available_memory": gpu.memoryFree
        })

    # Get total VRAM
    total_vram = sum(gpu.memoryTotal for gpu in GPUtil.getGPUs())

    return {
        "cpu": {
            "logical_cores": cpu_count,
            "physical_cores": cpu_cores
        },
        "gpus": gpus,
        "total_vram": total_vram
    }