
import json
import os
from pathlib import Path
from ntpath import exists
from part2_coding_agent_mvp.config.config import get_work_dir
from part2_coding_agent_mvp.tools.paths import resolve_work_path
from langchain.tools import tool

@tool
def list_files(path : str)->str:
    """
    List all the files and the directories  under the given path in the working directory 

    Args:
        path : Relative directory to list , default to the working directory root
    """

    work_dir  =get_work_dir

    try :
        base_path = resolve_work_path(path)
    except ValueError as err:
        return ValueError(f"Path escapes the working directory : {err}")

    if not base_path.exists():
        return json.dumps({
            "error" : f"Path -{path!r} doesnot exsists "
        })
    # when you list the files it should be inside the directory 
    if not base_path.is_dir():
        return json.dumps({
            "error" : f"Path -{path!r} is not a diretory "
        })

    
    result : list[str] = []


    for root, dirs ,files in os.walk(base_path):
        root_path = Path(root)
        rel_root =  root_path.relative_to(work_dir)

        for dir_name in sorted(dirs):
            result.append(f"{(rel_root / dir_name).as_posix()}/")
        
        for file_name in sorted(dirs):
            result.append(f"{(rel_root / file_name).as_posix()}/")

            
    return json.dumps(result)
    

