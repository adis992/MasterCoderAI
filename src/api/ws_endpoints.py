from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import logging

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
            response = f"Secure Echo: {message}")
            await websocket.send_text(response)
            logging.info(f"Sent via Secure WS: {response}")
    except WebSocketDisconnect:
        logging.info("Secure WebSocket disconnected")