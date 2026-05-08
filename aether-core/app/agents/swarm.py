from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.core.websocket import manager
from app.core.toolbox import toolbox
from app.core.memory import memory
from app.core.approvals import approval_manager
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
- architect: Designs systems, technical specs, and file structures.
- coder: Implements features, writes/reads files, and handles GitHub.
- marketer: Researches markets, handles Stripe, and defines business logic.

Relevant Context from Memory:
{context}

You should break down the goal into steps and delegate to the appropriate agent.
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
        # Get the last few messages for context
        history = messages[-5:]
        response = await llm.ainvoke([
            SystemMessage(content=CEO_PROMPT.format(context=context)),
            *history
        ])
        
        content = response.content
        try:
            if "{" in content:
                json_str = content[content.find("{"):content.rfind("}")+1]
                data = json.loads(json_str)
            else:
                data = json.loads(content)
            next_agent = data.get("next_agent", "architect")
            directive = data.get("directive", "Proceed with design.")
        except:
            # Heuristic fallback
            next_agent = "architect"
            directive = content

    await manager.broadcast({
        "type": "pulse",
        "agent": "CEO",
        "action": f"Strategy: {directive}",
        "timestamp": "Just now"
    })
    
    return {"next_agent": next_agent, "messages": [AIMessage(content=directive)]}

CODER_PROMPT = """You are the Aether Coder. You implement features and write code.
Available tools:
- read_file(path): Read the content of a file.
- write_file(path, content): Write content to a file.
- run_command(command): Run a shell command.
- create_github_repo(name): Create a new repository.

When you are ready to write code, describe your plan and then use the tools.
Objective: {goal}
Directive: {directive}"""

async def coder_node(state: AgentState):
    """The Coder agent uses LLM to write code or call tools."""
    goal = state.get("goal", "")
    directive = state["messages"][-1].content
    
    if not llm:
        action = "Coder: Simulation mode active."
    else:
        response = await llm.ainvoke([
            SystemMessage(content=CODER_PROMPT.format(goal=goal, directive=directive)),
            HumanMessage(content="Implement the requested change.")
        ])
        action = response.content
    
    # Simple heuristic to trigger tools for the prototype
    # In a real app, we would use LangChain's tool-calling support
    if "write_file" in action.lower() and "```" in action:
        # Extract code and path
        try:
            import re
            code_blocks = re.findall(r"```(?:\w+)?\n(.*?)\n```", action, re.DOTALL)
            path_match = re.search(r"path[:\s]+([\w\./-]+)", action)
            if code_blocks and path_match:
                path = path_match.group(1)
                content = code_blocks[0]
                await toolbox.call_tool("Coder", "write_file", {"path": path, "content": content})
                action = f"Successfully implemented changes in {path}"
        except Exception as e:
            action = f"Error during implementation: {str(e)}"

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
    """Wait for human intervention via the approval manager."""
    pending = state.get("pending_approvals", [])
    if not pending:
        return state
    
    approval_id = pending[0]["id"]
    approval_manager.create_approval(approval_id)
    
    await manager.broadcast({
        "type": "pulse",
        "agent": "SYSTEM",
        "action": f"Awaiting approval: {approval_id}",
        "timestamp": "Just now"
    })
    
    await approval_manager.wait_for_approval(approval_id)
    
    await manager.broadcast({
        "type": "pulse",
        "agent": "SYSTEM",
        "action": f"Approval granted: {approval_id}",
        "timestamp": "Just now"
    })
    
    return {"pending_approvals": []}

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
