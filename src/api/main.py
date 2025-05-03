import logging
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .middleware import LoggingMiddleware
from .ws_endpoints import router as ws_router

# Configure logging to file
logging.basicConfig(filename="mastercoderai.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(message)s")

# Inicijalizacija rate limiter-a
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.add_middleware(LoggingMiddleware)
# Dodavanje TrustedHost middleware-a za zaštitu od Host header napada
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"])
# Dodavanje SlowAPI middleware-a za integraciju rate limiting-a
app.add_middleware(SlowAPIMiddleware)
app.include_router(ws_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    logging.info(f"Chat request received: {message}")
    # Simple echo response
    response = {"response": f"Echo: {message}"}
    logging.info(f"Chat response sent: {response['response']}")
    return response

@app.get("/limited")
@limiter.limit("5/minute")
async def limited_endpoint():
    return {"message": "Ovaj endpoint je ograničen na 5 zahtjeva po minuti."}

@app.get("/secure-endpoint")
async def secure_endpoint():
    return {"message": "Ovo je siguran endpoint sa svim implementiranim mjerama."}