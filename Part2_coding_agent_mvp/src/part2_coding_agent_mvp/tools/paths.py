# # This file handles the model's perspective.

# If the model needs to create or modify a file after making a tool call,

# it needs to know the paths of the relevant files and how to create the new file.


from fnmatch import fnmatch
from pathlib import Path 
from part2_coding_agent_mvp.config import get_work_dir


BLOCKED_PATH_PATTERNS = [
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    ".git",
    ".git/**",
    "*.secret",
    "*.log",
    "*.p12",
]

def normalise_path(path :str) -> str:
    normalized = Path(path).as_posix()
    # Output: folder/subfolder/file.txt (POSIX string)
    # like compatable for both linux and the mac 
    if normalized.startswith("./"):
        normalized = normalized[2:]
        # if the path starts with ./ then it will trim 
    return normalized

def is_blocked_path(path:str) -> bool:
    normalized = normalise_path(path)
    return any(fnmatch (normalized , pattern) for pattern in BLOCKED_PATH_PATTERNS)

def resolve_work_path(path : str) ->Path :
    work_dir = get_work_dir()
    work_dir.mkdir(parents=True ,exist_ok=True)
    candidate = (work_dir/path).resolve()
    try :
        candidate.relative_to(work_dir)
    except ValueError  as e:
        raise ValueError(f"Path escapes working directory")
    return candidate

def ensure_path_safe(path: str) -> Path:
    """
    Runs both checks. If either fails, halts (raises). 
    If both pass, returns the safe, resolved path.
    """

    if is_blocked_path(path):
        raise ValueError(f"this is the blocked path :  {path}")

    safe_path = resolve_work_path(path)

    return safe_path

