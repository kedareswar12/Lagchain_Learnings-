
from part2_coding_agent_mvp.tools.edit_file import edit_file
from part2_coding_agent_mvp.tools.list_files import list_files
from part2_coding_agent_mvp.tools.read_file import read_file
from part2_coding_agent_mvp.tools.write_file import write_file


ALL_TOOLS = [
    write_file,
    edit_file,
    list_files,
    read_file

]


def tool_catalog() -> list[dict[str, str]]:
    """Name + Description for all tools"""
    return [{"name": tool.name, "description": tool.description} for tool in ALL_TOOLS]