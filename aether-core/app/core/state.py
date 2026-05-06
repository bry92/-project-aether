from typing import Annotated, TypedDict, List, Union
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # The messages in the conversation
    messages: Annotated[list, add_messages]
    # The specialized agent currently in control
    next_agent: str
    # A list of completed tasks
    completed_tasks: List[str]
    # A list of pending approvals
    pending_approvals: List[dict]
    # The overall goal of the thread
    goal: str
    # Contextual memory for the thread
    memory: dict
