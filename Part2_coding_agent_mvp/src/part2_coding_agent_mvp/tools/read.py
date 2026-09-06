from langchain_core.tools import tool
from part2_coding_agent_mvp.tools.paths import resolve_work_path

@tool
def read_file(path:str)-> str:
    """
    Read the UTF-8 Encoded file  from the working directory 

    Agrs: 
        path:Relative path of the file eg; src/App.js or 'Readme.md' etc

    """

    try:
        file_path= resolve_work_path(path)

    except ValueError as err:
        raise ValueError(f"Path escapes the working directory : {err}")

    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"file not found {path}")
    except PermissionError:
        raise PermissionError(f"Dont have the permisiion to read the file{path}")
    except Exception as err :
        raise Exception(f"Error in handling the file {err}")
