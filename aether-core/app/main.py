from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from app.core.websocket import manager
from app.core.engine import process_task
import asyncio
import json

app = FastAPI(title="Aether Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Aether Core is operational", "version": "0.1.0"}

@app.post("/tasks/execute")
async def execute_task(payload: dict = Body(...)):
    task = payload.get("task")
    if not task:
        return {"error": "No task description provided"}, 400
    
    # Run task in background to not block the request
    asyncio.create_task(process_task(task))
    return {"status": "Task queued for execution", "task": task}

@app.websocket("/ws/pulse")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and wait for client messages if any
            data = await websocket.receive_text()
            # Echo or handle client message
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to simulate agent activity for the Live Pulse
async def simulate_pulse():
    agents = ["CEO", "Architect", "Coder", "Marketer", "Tester"]
    actions = [
        "Analyzing market trends for autonomous startups.",
        "Refining the multi-agent state machine.",
        "Implementing glass-morphic UI components.",
        "Executing security vibe check on core logic.",
        "Generating production deployment plan."
    ]
    
    while True:
        import random
        agent = random.choice(agents)
        action = random.choice(actions)
        
        await manager.broadcast({
            "type": "pulse",
            "agent": agent,
            "action": action,
            "timestamp": "Just now"
        })
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_pulse())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
