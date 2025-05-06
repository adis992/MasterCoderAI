from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging
import json  # for task data
from .db import database
from .models import tasks
from .auth import get_current_user

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("WebSocket connection accepted")
    try:
        while True:
            message = await websocket.receive_text()
            logging.info(f"Received via WS: {message}")
            response = f"Echo: {message}"
            await websocket.send_text(response)
            logging.info(f"Sent via WS: {response}")
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")

@router.websocket("/ws/secure")
async def secure_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("Secure WebSocket connection accepted")
    try:
        while True:
            message = await websocket.receive_text()
            logging.info(f"Received via Secure WS: {message}")
            response = f"Secure Echo: {message}"
            await websocket.send_text(response)
            logging.info(f"Sent via Secure WS: {response}")
    except WebSocketDisconnect:
        logging.info("Secure WebSocket disconnected")

@router.websocket("/ws/tasks")
async def tasks_websocket(websocket: WebSocket):
    # Authenticate via token query param
    token = websocket.query_params.get('token')
    if not token:
        await websocket.close(code=1008)
        return
    try:
        current_user = await get_current_user(token)
    except:
        await websocket.close(code=1008)
        return
    user_id = current_user['id']
    await websocket.accept()
    try:
        while True:
            data_text = await websocket.receive_text()
            task_data = json.loads(data_text)
            # Store task with pending status
            insert = tasks.insert().values(user_id=user_id, task_data=task_data, status='pending')
            task_id = await database.execute(insert)
            # Notify client
            await websocket.send_text(json.dumps({"status": "received", "task_id": task_id}))
            # Simulate processing steps
            steps = ['parsing', 'executing', 'finalizing']
            for step in steps:
                # Update status in DB
                await database.execute(tasks.update().where(tasks.c.id == task_id).values(status=step))
                await websocket.send_text(json.dumps({"status": step, "task_id": task_id}))
            # Mark completed
            await database.execute(tasks.update().where(tasks.c.id == task_id).values(status='completed'))
            await websocket.send_text(json.dumps({"status": "completed", "task_id": task_id}))
    except WebSocketDisconnect:
        pass