import subprocess
import shlex
from part2_coding_agent_mvp.config.config import get_work_dir
from part2_coding_agent_mvp.tools.paths import is_blocked_path

DEFAULT_TIMEOUT_SECONDS = 40

BLOCKED_COMMANDS = {
    "rm", "rmdir", "sudo", "su", "chmod", "chown",
    "shutdown", "reboot", "mkfs", "dd",
}

def run_command(command :str ,  timeout: int = DEFAULT_TIMEOUT_SECONDS)-> str:
    """
    Run a shell command inside the working directory and return its output.
    Guardrails:
        - Runs with the working directory as cwd, never outside it.
        - Never runs through a shell (no `shell=True`), so things like `&&`,
          `;`, `|`, or `$(...)` are treated as literal arguments, not chained
          commands. This blocks the classic shell-injection escape.
        - Refuses a fixed list of destructive commands (rm, sudo, chmod, etc.).
        - Long-running/blocking processes (servers) are killed and reported
          as timed out rather than hanging the agent forever. For something
          you intend to leave running (like a dev server), use
          `run_command_background` instead of this one.

    Args:
        command: The command to run, e.g. "pytest -q" or "uvicorn main:app --port 8000".
        timeout: Max seconds to let the command run before it's killed. Defaults to 60.
    
    """

    if not command or not command.strip():
        return "Error: command is required , Enter the valid command"
    try:
        parts = shlex.split(command)
    except ValueError as err:
        return f"the command entered cannot be parsed  : {err}"

    if not parts:
        return "Error: command is required"

    program = parts[0].lower()

    if program in BLOCKED_COMMANDS or is_blocked_path(program):
        return f"Error: {program!r} is not allowed to run through this tool"

    work_dir = get_work_dir()
    work_dir.makdir(parents= True , exist_ok= True)


    try:
        result = subprocess.run(
            parts,
            cwd= work_dir,
            shell=False,
            capture_output=True,
            text = True,
            timeout= timeout
        )
    except FileNotFoundError:
        return f"Error: program {program!r} was not found"
    except subprocess.TimeoutExpired:
         return (
            f"Error: command timed out after {timeout}s. "
            "If this was meant to keep running (like a server), "
            "use run_command_background instead."
        )
    except Exception as err:
        return f"Error: failed to run command: {err}"

    output = (
        f"exit code: {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )
    return output[:8000]