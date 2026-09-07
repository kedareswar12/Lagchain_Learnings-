
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

def user_input(text:str) -> dict[str,str]:
    """
    this is written in this way because see the documntation of the langchain it preferres the open ai type 
    format so we have written like this 
    
    """
    return {
        "role" : "User",
        "content" : {text}
    }

"""
result["messages"][-1].content

normally this will be the last  ai message 
Problems 

1. Last message might be a tool result, not from the AI at all
2. 	Might be a tool-call-only turn with no real text
3. Some providers return content as a list of typed blocks, not a plain string

this fxn makes smooth over all three of those inconsistencies in one place
"""


"""

"""
def last_ai_text(messages : list[Any]) -> str:
    """this function will give you the last ai messsage that is not a tool call only turn """

    for message in reversed(messages):
        if not isinstance(message , AIMessage):
            continue
        if getattr(message , "tool_calls" , None):
            continue
        content  = message.content
        if isinstance(content, str ):
            return content
        if isinstance(content , list):
            parts = [
                block.get ("text" , "")for block in content if isinstance(block,dict) and block.get("type") == "text"
            ]
            return "\n".join(part for part in parts if part)

    return ""

# adding a loggable utility
def last_tool_text(messages: list[Any]) -> str:
    """
    Return the content of the most recent tool result 
    useful when the model skips the chat reply 
    """
    for message in reversed(messages):
        if isinstance(message , ToolMessage):
            content = message.content
            return content if isinstance(content ,str) else str(content)

    return ""



def describe_message(message : str) -> str :
    role = type(message).__name__.replace("Message", "").lower()
    content = message.content
    preview = content if isinstance(content , str) else str(content)
    preview = preview.replace("\n" , " ")

    if isinstance(message , AIMessage) and message.tool_calls:
        names = ", ".join(call.get("name" , "?") for call in message.tool_calls)
        extra = f" tools = {[names]}"

    if isinstance(message , ToolMessage):
        extra = f" tool_call_id = {message.tool_call_id}"

    if isinstance(message, SystemMessage):
        extra = f"(system)"

    if isinstance(message, HumanMessage):
        extra = f"(human)"

    return f"{role}{extra} : {preview}"