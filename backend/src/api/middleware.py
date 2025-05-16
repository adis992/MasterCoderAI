# Middleware for logging HTTP requests and responses
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.cors import CORSMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger = logging.getLogger()
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {request.method} {request.url} - {response.status_code}")
        return response