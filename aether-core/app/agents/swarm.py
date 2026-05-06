from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.core.websocket import manager
from app.core.toolbox import toolbox
import json

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", streaming=True)

async def ceo_node(state: AgentState):
    """The CEO agent routes tasks and manages overall project state."""
    messages = state["messages"]
    last_message = messages[-1].content.lower()
    
    # Simple logic for routing
    next_agent = "architect" 
    if any(k in last_message for k in ["code", "fix", "commit", "github"]):
        next_agent = "coder"
    elif any(k in last_message for k in ["market", "sell", "stripe", "buy", "browser"]):
        next_agent = "marketer"
    
    await manager.broadcast({
        "type": "pulse",
        "agent": "CEO",
        "action": f"Strategizing objective. Delegating to {next_agent.capitalize()}.",
        "timestamp": "Just now"
    })
    
    return {"next_agent": next_agent}

async def coder_node(state: AgentState):
    """The Coder agent implements features and interacts with GitHub."""
    goal = state.get("goal", "").lower()
    
    if "github" in goal or "repo" in goal:
        # Simulate repository creation logic
        repo_name = f"aether-project-{json.dumps(goal)[:10].replace(' ', '-')}"
        result = await toolbox.call_tool("Coder", "create_github_repo", {"name": repo_name})
        action = f"Created repository: {repo_name}"
    else:
        action = "Implementing full-stack features and writing unit tests."
    
    await manager.broadcast({
        "type": "pulse",
        "agent": "Coder",
        "action": action,
        "timestamp": "Just now"
    })
    return {"messages": [("assistant", f"Coder: {action}")]}

async def marketer_node(state: AgentState):
    """The Marketer agent researches markets and handles payments."""
    goal = state.get("goal", "").lower()
    
    if "browse" in goal or "market" in goal:
        # Simulate browser research
        result = await toolbox.call_tool("Marketer", "capture_page", {"url": "https://news.ycombinator.com"})
        action = "Conducting market research via autonomous browser control."
    elif "stripe" in goal or "payment" in goal:
        result = await toolbox.call_tool("Marketer", "create_checkout_session", {"product_name": "Aether Pro", "amount": 9900})
        action = "Configuring Stripe checkout sessions for monetization."
    else:
        action = "Drafting marketing copy and SEO strategy."

    await manager.broadcast({
        "type": "pulse",
        "agent": "Marketer",
        "action": action,
        "timestamp": "Just now"
    })
    return {"messages": [("assistant", f"Marketer: {action}")]}

async def architect_node(state: AgentState):
    """The Architect agent designs the technical solution."""
    await manager.broadcast({
        "type": "pulse",
        "agent": "Architect",
        "action": "Designing scalable architecture and multi-agent protocols.",
        "timestamp": "Just now"
    })
    return {"messages": [("assistant", "Architect: Architecture finalized.")]}

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("ceo", ceo_node)
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("marketer", marketer_node)

workflow.set_entry_point("ceo")

def route_from_ceo(state: AgentState):
    return state["next_agent"]

workflow.add_conditional_edges(
    "ceo",
    route_from_ceo,
    {
        "architect": "architect",
        "coder": "coder",
        "marketer": "marketer"
    }
)

workflow.add_edge("architect", END)
workflow.add_edge("coder", END)
workflow.add_edge("marketer", END)

graph = workflow.compile()
