from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from bot import Bot
import uvicorn
from typing import Dict

app = FastAPI(title="MasterCoder AI Bot")
bot = Bot()

@app.get("/")
async def root():
    return {"message": "MasterCoder AI Bot API"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    response = bot.generate_response(message)
    return {"response": response}

@app.post("/review")
async def review_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    suggestion = bot.get_code_suggestion(code)
    return {"suggestion": suggestion}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            response = bot.generate_response(message)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)