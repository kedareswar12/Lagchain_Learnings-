from datetime import datetime , UTC
import json
from langchain.agents.middleware import AgentMiddleware
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable ,Any 
from langchain.messages import ToolMessage 
from langgraph.types import Command

from part2_coding_agent_mvp.config.config import get_work_dir




class AuditMiddleware(AgentMiddleware):
    """Append the JSON record after each tool call (allowed or denied)"""

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]) -> ToolMessage | Command[Any]:

        response = handler(request)#make the tool call 
        preview = ""
        if isinstance(response , ToolMessage):
            preview = str(response.content)[:200]

        self._write({
            "tiemstamp": datetime.now(UTC).isformat(),
            "tool" : request.tool_call.get('name'),
            "response_preview" : preview,
            "arguments" : request.tool_call.get('args'),
        })
        
    def _write(
        self,
        entry : dict[str  ,Any]
        )  -> None:
        log_path = get_work_dir()/".agent_audit.log"
        log_path.parent.mkdir(parents=True , exist_ok=True)
        with log_path.open("a" , encoding='utf8') as f :
            f.write(json.dumps(entry) + "\n")







        