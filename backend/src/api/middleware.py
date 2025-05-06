# Middleware for logging HTTP requests and responses
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

# Inicijalizacija rate limiter-a
limiter = Limiter(key_func=get_remote_address)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger()
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {request.method} {request.url} - {response.status_code}")
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        limiter.check(request)
        response = await call_next(request)
        return response

# Dodavanje HTTPS middleware-a za osiguranje šifriranja podataka
app.add_middleware(HTTPSRedirectMiddleware)

# Dodavanje rate limiting middleware-a
app.add_middleware(RateLimitMiddleware)

# Dodavanje CORS middleware-a za omogućavanje zahtjeva iz različitih domena
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Promijeniti na specifične domene u produkciji
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)