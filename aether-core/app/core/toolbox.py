from app.api.github import github
from app.api.browser import browser
from app.api.stripe import stripe
from app.core.tools import run_shell_command, write_to_file
from app.core.websocket import manager
from app.core.supabase import supabase
from typing import Dict, Any
import os
import uuid

class AgentToolbox:
    @staticmethod
    async def call_tool(agent_name: str, tool_name: str, params: Dict[str, Any]):
        """Execute a tool and broadcast the action to the Live Pulse."""
        
        await manager.broadcast({
            "type": "pulse",
            "agent": agent_name,
            "action": f"Executing tool: {tool_name} with params {params}",
            "timestamp": "Just now"
        })

        try:
            if tool_name == "create_github_repo":
                return github.create_repo(**params)
            elif tool_name == "commit_files":
                return github.commit_files(**params)
            elif tool_name == "capture_page":
                return await browser.capture_page(**params)
            elif tool_name == "create_checkout_session":
                return stripe.create_checkout_session(**params)
            elif tool_name == "read_file":
                path = params.get("path")
                # Safety check: keep it within project root
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                full_path = os.path.join(root_dir, path)
                if not os.path.exists(full_path):
                    return f"Error: File {path} not found."
                with open(full_path, "r") as f:
                    return f.read()
            elif tool_name == "write_file":
                path = params.get("path")
                content = params.get("content")
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                full_path = os.path.join(root_dir, path)
                
                # If it's a creative asset, also store in Supabase for the UI
                if "creatives/" in path:
                    try:
                        supabase.table("assets").insert({
                            "id": str(uuid.uuid4()),
                            "type": "script",
                            "title": os.path.basename(path),
                            "content": content,
                            "agent": agent_name
                        }).execute()
                    except Exception as e:
                        print(f"Supabase asset store error: {e}")

                return write_to_file(full_path, content)
            elif tool_name == "run_command":
                command = params.get("command")
                return run_shell_command(command)
            else:
                return f"Error: Tool {tool_name} not found."
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            await manager.broadcast({
                "type": "pulse",
                "agent": "SYSTEM",
                "action": error_msg,
                "timestamp": "Just now"
            })
            return error_msg

toolbox = AgentToolbox()
