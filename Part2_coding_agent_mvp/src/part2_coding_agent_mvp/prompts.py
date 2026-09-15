from pkgutil import extend_path
from jinja2 import Environment , FileSystemLoader , select_autoescape
from part2_coding_agent_mvp.config.config import AGENT_NAME, PROMPTS_DIR, get_work_dir
from part2_coding_agent_mvp.tools import tool_catalog


_env= Environment(
    loader= FileSystemLoader(PROMPTS_DIR), 
    autoescape= select_autoescape(enabled_extensions=()),
    trim_blocks= True,
    lstrip_blocks= True,

)
def render_template (name:str , **context :str)-> str:
    return _env.get_template(name).render(**context)

def build_prompt(
    *,
    agent_name: str = AGENT_NAME,
    extra_guidance : str = "" ,
    )-> str:
        return render_template(
            "system_prompt.jinja" ,
             agent_name=agent_name  ,
              extra_guidance = extra_guidance ,
               work_dir = get_work_dir(),
               tools = tool_catalog())

def build_greeting(
    *,
    agent_name : str =AGENT_NAME )-> str:
    return render_template(
        "greeting.jinja",
        agent_name = agent_name,
        work_dir =str( get_work_dir())
    )


