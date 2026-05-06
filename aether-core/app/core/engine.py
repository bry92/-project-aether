from app.agents.swarm import graph
from app.core.state import AgentState
from app.core.websocket import manager
from app.core.memory import memory
from langchain_core.messages import HumanMessage
import uuid

async def process_task(task_description: str, thread_id: str = None):
    """Entry point for the agentic swarm to process a user task."""
    if not thread_id:
        thread_id = str(uuid.uuid4())
    
    # 1. Store the goal in memory
    memory.store(task_description, {"thread_id": thread_id, "type": "goal"})
    
    # 2. Initialize state
    state = {
        "messages": [HumanMessage(content=task_description)],
        "next_agent": "ceo",
        "completed_tasks": [],
        "pending_approvals": [],
        "goal": task_description,
        "memory": {}
    }
    
    # 3. Execute the swarm (LangGraph)
    # Note: In a real app, this would be a stream or a background process
    await manager.broadcast({
        "type": "pulse",
        "agent": "SYSTEM",
        "action": f"Task initiated: {task_description}",
        "timestamp": "Just now"
    })
    
    # Run the graph
    async for event in graph.astream(state):
        # We can broadcast granular updates here if needed
        pass

    await manager.broadcast({
        "type": "pulse",
        "agent": "SYSTEM",
        "action": "Task sequence finalized.",
        "timestamp": "Just now"
    })
    
    return {"status": "Task processed", "thread_id": thread_id}
