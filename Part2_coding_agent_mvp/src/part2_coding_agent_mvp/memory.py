
from langgraph.checkpoint.memory import InMemorySaver

def make_checkpointer() -> InMemorySaver:
    return InMemorySaver()

def thread_config(thread_id : str) ->dict :
    return{
        "configurable" : {
            "thread_id" : thread_id
        }
    }