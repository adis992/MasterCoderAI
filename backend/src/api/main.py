import logging
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .middleware import LoggingMiddleware
from .ws_endpoints import router as ws_router
from .auth import router as auth_router, get_current_user
from .db import database
from .models import users, chats
from passlib.context import CryptContext

# Configure logging to file
logging.basicConfig(filename="mastercoderai.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")

# Inicijalizacija rate limiter-a
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.include_router(auth_router)
app.add_middleware(LoggingMiddleware)
# Dodavanje TrustedHost middleware-a za zaštitu od Host header napada
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"])
# Dodavanje SlowAPI middleware-a za integraciju rate limiting-a
app.add_middleware(SlowAPIMiddleware)
app.include_router(ws_router)

# Database connect/disconnect and user seeding
@app.on_event("startup")
async def startup():
    await database.connect()
    # Ensure admin and test user exist
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
    for username, password, is_admin in [("admin", "admin", True), ("user", "user", False)]:
        query = users.select().where(users.c.username == username)
        existing = await database.fetch_one(query)
        if not existing:
            hashed = pwd.hash(password)
            await database.execute(users.insert().values(
                username=username, hashed_password=hashed, is_admin=is_admin
            ))

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: Request, current_user=Depends(get_current_user)):
    data = await request.json()
    message = data.get("message", "")
    logging.info(f"Chat request from {current_user['username']}: {message}")
    # Simple echo or actual AI call
    resp_text = f"Echo: {message}"
    # Save chat
    await database.execute(chats.insert().values(
        user_id=current_user['id'], message=message, response=resp_text
    ))
    logging.info(f"Chat response sent: {resp_text}")
    return {"response": resp_text}

@app.get("/chats")
async def get_chats(current_user=Depends(get_current_user)):
    query = chats.select().where(chats.c.user_id == current_user['id']).order_by(chats.c.timestamp)
    results = await database.fetch_all(query)
    return [{"id": r['id'], "message": r['message'], "response": r['response'], "timestamp": r['timestamp'].isoformat()} for r in results]

@app.get("/limited")
@limiter.limit("5/minute")
async def limited_endpoint():
    return {"message": "Ovaj endpoint je ograničen na 5 zahtjeva po minuti."}

@app.get("/secure-endpoint")
async def secure_endpoint():
    return {"message": "Ovo je siguran endpoint sa svim implementiranim mjerama."}