from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.core.websocket import manager
from app.core.toolbox import toolbox
from app.core.memory import memory
import json
import uuid
import os

# Initialize LLM with Hugging Face
def get_llm():
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_token or hf_token == "your_huggingface_token_here":
        # Fallback to OpenAI if HF token is missing but OpenAI is present
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_key_here":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o", streaming=True)
        return None
    
    # Use Llama-3-8B-Instruct on Hugging Face
    endpoint = HuggingFaceEndpoint(
        repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        huggingfacehub_api_token=hf_token
    )
    return ChatHuggingFace(llm=endpoint)

llm = get_llm()

CEO_PROMPT = """You are the Aether CEO. Your job is to analyze the project goal and delegate tasks.
Available specialized agents:
- architect: Designs systems and technical specs.
- coder: Implements features and handles GitHub.
- marketer: Researches markets and handles Stripe payments.

Relevant Context from Memory:
{context}

Choose the next_agent and provide a clear directive.
Response format: JSON with "next_agent" and "directive" fields. Ensure you ONLY output JSON."""

async def ceo_node(state: AgentState):
    """The CEO agent uses LLM and Memory to strategize."""
    messages = state["messages"]
    goal = state.get("goal", "")
    
    # Retrieve context from memory
    context = memory.query(goal, n_results=3)
    
    if not llm:
        # Mock logic if no API key
        next_agent = "architect"
        directive = "Model provider token missing. Simulation mode active."
    else:
        response = await llm.ainvoke([
            SystemMessage(content=CEO_PROMPT.format(context=context)),
            *messages
        ])
        
        content = response.content
        # Hugging Face models sometimes output extra text, attempt to find JSON
        try:
            if "{" in content:
                json_str = content[content.find("{"):content.rfind("}")+1]
                data = json.loads(json_str)
            else:
                data = json.loads(content)
            next_agent = data.get("next_agent", "architect")
            directive = data.get("directive", "Proceed with design.")
        except:
            # Heuristic fallback if JSON parsing fails
            content_lower = content.lower()
            if "coder" in content_lower: next_agent = "coder"
            elif "marketer" in content_lower: next_agent = "marketer"
            else: next_agent = "architect"
            directive = content

    await manager.broadcast({
        "type": "pulse",
        "agent": "CEO",
        "action": f"Strategy: {directive}",
        "timestamp": "Just now"
    })
    
    return {"next_agent": next_agent, "messages": [AIMessage(content=directive)]}

async def coder_node(state: AgentState):
    """The Coder agent uses LLM to write code or call tools."""
    goal = state.get("goal", "")
    
    if not llm:
        action = "Coder: Simulation mode active. API Key required for real reasoning."
    else:
        prompt = f"Objective: {goal}. You are the Coder. If you need to create a repo or commit, say so. Otherwise, describe your implementation plan."
        
        response = await llm.ainvoke([
            SystemMessage(content="You are the Coder agent for Aether."),
            HumanMessage(content=prompt)
        ])
        action = response.content
    
    # Simple tool-triggering logic for prototype
    if "repo" in action.lower() or "github" in action.lower():
        repo_name = f"aether-build-{int(uuid.uuid4().hex[:8], 16)}"
        await toolbox.call_tool("Coder", "create_github_repo", {"name": repo_name})
        action = f"Created GitHub repository: {repo_name}"

    await manager.broadcast({
        "type": "pulse",
        "agent": "Coder",
        "action": action,
        "timestamp": "Just now"
    })
    return {"messages": [AIMessage(content=action)]}

async def marketer_node(state: AgentState):
    """The Marketer agent uses LLM to handle business ops."""
    goal = state.get("goal", "")
    
    if not llm:
        action = "Marketer: Simulation mode active."
    else:
        response = await llm.ainvoke([
            SystemMessage(content="You are the Marketer agent for Aether."),
            HumanMessage(content=f"Objective: {goal}")
        ])
        action = response.content
    
    if "market" in action.lower() or "browse" in action.lower():
        await toolbox.call_tool("Marketer", "capture_page", {"url": "https://news.ycombinator.com"})
    
    await manager.broadcast({
        "type": "pulse",
        "agent": "Marketer",
        "action": action,
        "timestamp": "Just now"
    })
    return {"messages": [AIMessage(content=action)]}

async def architect_node(state: AgentState):
    """The Architect agent designs systems."""
    goal = state.get("goal", "")
    
    if not llm:
        action = "Architect: Architecture finalized (Simulation)."
    else:
        response = await llm.ainvoke([
            SystemMessage(content="You are the Architect agent for Aether."),
            HumanMessage(content=f"Objective: {goal}")
        ])
        action = response.content
    
    # Request approval for the design
    pending_approval = {
        "id": str(uuid.uuid4()),
        "agent": "Architect",
        "description": "Approve the technical architecture design.",
        "details": action
    }

    await manager.broadcast({
        "type": "pulse",
        "agent": "Architect",
        "action": action,
        "timestamp": "Just now"
    })
    
    await manager.broadcast({
        "type": "approval_required",
        "approval": pending_approval
    })

    return {"messages": [AIMessage(content=action)], "pending_approvals": [pending_approval]}

async def human_approval_node(state: AgentState):
    """A dummy node that acts as a placeholder for human intervention."""
    return state

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("ceo", ceo_node)
workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("marketer", marketer_node)
workflow.add_node("human_approval", human_approval_node)

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

# After architect/coder/marketer, always go to human_approval
workflow.add_edge("architect", "human_approval")
workflow.add_edge("coder", "human_approval")
workflow.add_edge("marketer", "human_approval")

# From human_approval, it goes to END for now (in a real app, it would loop back or proceed)
workflow.add_edge("human_approval", END)

graph = workflow.compile()
