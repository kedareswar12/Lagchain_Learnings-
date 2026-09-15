from ast import arguments
from langchain.agents.middleware import AgentMiddleware
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable  ,Any
from langgraph.types import Command
import re 
from part2_coding_agent_mvp.tools.paths import is_blocked_path, resolve_work_path



_FILE_TOOLS = {
    "read_file",
    "write_file",
    "edit_file",
    "list_files"
}

BLOCKED_EDIT_PATTERNS = (
    r"\bos\.system\s*\(",
    r"\bsubprocess\b",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"__import__\s*\(",
)

def _tool_message(request : ToolCallRequest , reason :str)-> ToolMessage:
    return ToolMessage(
        content = reason,
        tool_call_id = request.tool_call['id'],
        name = request.tool_call["name"]

    )

def deny_reason(tool_name : str , arguments : dict[str, Any]) -> str | None:

    """Return a denial reason or None if call may proceed """
    if tool_name not in _FILE_TOOLS:
        return None
    
    path = arguments.get("path" , ".")
    if is_blocked_path(str(path)):
        return (f"Blocked by the middleware : access to the protected path {path} is not allowed")


    if tool_name == 'read_file':
        try:
            file_path = resolve_work_path(str(path))

        except ValueError as err:
            return f"Blocked by middleware : {err}"

        if file_path.is_file() and file_path.stat().st_size > 1024 * 10:  #10mb
            return (f"Blocked by the middleware : File size is too large to read.")

    payload = ""
    if tool_name == 'edit_file':
        payload = str(arguments.get("new_str" , ""))
    elif tool_name == 'write_file':
        payload = str(arguments.get("content" , ""))

    if payload:
        for pattern in BLOCKED_EDIT_PATTERNS:
            if re.search(pattern, payload ,re.IGNORECASE):
                return (
                    f"Blocked by the middleware : suspicious paylod detected."
                )



class Protection_Middleware(AgentMiddleware):
    """ going to short circuit the tool calls that target secrets or dangerous payload """

    def wrap_tool_call(self,
     request: ToolCallRequest,
     handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]) -> ToolMessage | Command[Any]:

     name = request.tool_call.get('name' , "")
     arguments = request.tool_call.get('args' , {})


     reason = deny_reason(name ,arguments)
     if reason is not None:
        return _tool_message(request , reason)

        return handler(request)

