# API

The API module provides RESTful and WebSocket endpoints for interacting with the MasterCoderAI system. It is built using FastAPI and includes middleware for request handling.

## Features
- RESTful API endpoints
- WebSocket support
- Middleware for request processing

## Usage
Run the API server:
```bash
uvicorn src.api.main:app --reload
```

Access the API documentation at `http://127.0.0.1:8000/docs`.