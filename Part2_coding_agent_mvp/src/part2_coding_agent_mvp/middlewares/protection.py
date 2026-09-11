from ast import arguments
from langchain.agents.middleware import AgentMiddleware
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable  ,Any
from langgraph.types import Command


def deny_reason(tool_name : str , arguments : dict[str, Any]) -> str | None:

    """Return a denial reason or None if call may proceed """
    


class Protection_Middleware(AgentMiddleware):
    """ going to short circuit the tool calls that target secrets or dangerous payload """

    def wrap_tool_call(self,
     request: ToolCallRequest,
     handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]) -> ToolMessage | Command[Any]:

     name = request.tool_call.get('name' , "")
     arguments = request.tool_call.get('args' , {})

