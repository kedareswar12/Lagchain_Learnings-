from dataclasses import dataclass, field
from typing import Any
import os
import contextlib
import signal
import subprocess
from pathlib import Path
import datetime

from datetime import UTC
@dataclass
class BackgroundJob:
    pid: int
    command: str
    started_at: str
    log_path: str
    proc: Any = field(default=None, repr=False)


# in-memory registry: pid -> job
_JOBS: dict[int, BackgroundJob] = {}


def register(job: BackgroundJob) -> None:
    _JOBS[job.pid] = job


def get_pid(pid: int) -> BackgroundJob | None:
    return _JOBS.get(pid)


def all_jobs() -> list[BackgroundJob]:
    return list(_JOBS.values())


def remove(pid: int) -> BackgroundJob | None:
    return _JOBS.pop(pid, None)


def is_alive(pid: int) -> bool:
    job = get_pid(pid)
    if job is not None and job.proc is not None:
        return job.proc.poll() is None  # None means still running

    # No Popen handle: fall back to checking the pid directly
    try:
        os.kill(pid, 0)  # signal 0 = existence check, sends nothing ,just checking not killing 
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, but owned by another user
    return True

def stop_pid(pid:int)->str:
    job = get_pid(pid)
    
    if job is None:
        return f"Error : {pid} is not a job started by this agent "
    
    if not is_alive(pid):
        if job.proc is not None:
            with contextlib.supress(ChildProcessError):
                job.proc.wait(timeout = 0.1)
                
        remove(pid)
        return f"Job {pid} is already stopped"

    try:
        os.killpg(pid , signal.SIGTERM)
    except ProcessLookupError:
        remove(pid)
        return f"Jobs {pid} is already stopped"
    except PermissionError as err:
        return f"Error stoppin the job {pid} : {err}"
    
    if job.proc is not None:
        try:
            job.proc.wait(timeout=1.5)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(pid, signal.SIGKILL)
            with contextlib.suppress(subprocess.TimeoutExpired):
                job.proc.wait(timeout=1)
    remove(pid)
    return f"Sent SIGTERM to process group {pid} ({job.command!r})."

def read_log_tail(log_path: Path, *, max_chars: int = 4000) -> str:
    if not log_path.is_file():
        return ""
    text = log_path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[-max_chars:]
    return text


def now_iso() -> str:
    return datetime.now(UTC).isoformat()