from pathlib import Path
import os 
from dotenv import load_dotenv
load_dotenv()


# actually the src is stored as the root of the project 
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
# print(PROJECT_ROOT)

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"

# since the coding agent will create all the files we are going to giive it a workspace directory so that it will work in that particular space 
DEFAULT_WORK_DIR = Path(__file__).resolve().parent.parent.parent / "workspace"


AGENT_NAME= "Kedar Personal Agent"

MAX_MODEL_CALLS_PER_RUNS = int(os.getenv("MAX_MODEL_CALLS_PER_RUNS" ,"10"))

MAX_READ_BITES = int(os.getenv("MAX_READ_BITES",10^6))

def hitl_enabled() -> bool:
    return os.getenv("HITL_ENABLED" , "true").lower() in {1, "yes" , "y" , "true"}

def get_work_dir() -> Path:
    # if you have any exsisting workspace use that else use the default one 
    override = os.getenv("WORK_DIR", "").strip()
    # it says if override means there is an exsisting work directory  
    if override:
        return Path (override).expanduser().resolve()
        # expnduser will solve the ~\users all the problems try to google it for better understanding 

    return DEFAULT_WORK_DIR.resolve()