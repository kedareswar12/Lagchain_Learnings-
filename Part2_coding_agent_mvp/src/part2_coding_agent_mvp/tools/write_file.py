from langchain_core.tools import tool
from part2_coding_agent_mvp.tools.paths import resolve_work_path
from part2_coding_agent_mvp.tools.text import prepare_file_content

@tool 
def write_file(path:str , content :str)->str:
    """
    Create or overwrite a UTF-8 text file in the working directory.

    Works for any text file (.js, .java, .py etc).
    `contet` is the full file body with real newline characters between lines. Do not wrap it 
    in markdown fence. Do not encode line breads as the two-character sequence backslash-n.

    Args:
        path: Relative path of the file to create/overwrite (e.g. "README.md")
        content: Full file body with real newlines. No markdown fence. No backslash-n encoding.

    """
    if not path:
        return "path is requried"
    
    content = prepare_file_content (path ,content)
    try : 
        file_path  = resolve_work_path(path)
    except ValueError as err :
        return f"Error: Path escaped working directory : {err}"

    try: 
        file_path.parent.mkdir(parents =True , exist_ok= True)
        file_path.write_text(content ,encoding="utf-8")
    except Exception as err:
        return f"Error : Failed to write file{path!r} : {err}"
    
    return f"File {path!r} written successfully "
