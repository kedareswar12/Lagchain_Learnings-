from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.structured_output import ProviderStrategy
from part2_coding_agent_mvp.config.config import MAX_MODEL_CALLS_PER_RUNS, hitl_enabled
from part2_coding_agent_mvp.middlewares.audit import AuditMiddleware
from part2_coding_agent_mvp.middlewares.protection import Protection_Middleware
from part2_coding_agent_mvp.middlewares.hitl import HumanInTheLoopMiddleware
from part2_coding_agent_mvp.models import build_chat_model
from part2_coding_agent_mvp.prompts import build_prompt, build_system_prompt
from part2_coding_agent_mvp.schemas import TurnSummary
from part2_coding_agent_mvp.tools import ALL_TOOLS



def build_middleware(
    *,
    enable_hitl :bool
    ) -> list:
    """
    This is the harness layers , outermost layer first

    1. model-call-cap 
    2. Audit log
    3. payload gaurding 
    4. HITL on write/edit/run

    """

    layers:list=[
        ModelCallLimitMiddleware(
            run_limit = MAX_MODEL_CALLS_PER_RUNS,
            exit_behavior="end"
        ),
        AuditMiddleware (),
        Protection_Middleware()
        
    ]

    if enable_hitl:
        layers.append(HumanInTheLoopMiddleware)

    return layers 

def build_agent(
    *,
    enable_hitl : bool | None  = None,
    extra_guidance: str = "",
    ):
    model , provider  = build_chat_model()
    use_hitl = hitl_enabled () if enable_hitl is None else enable_hitl
    return create_agent(
        model= model,
        tools= ALL_TOOLS,
        system_prompt = build_system_prompt(extra_guidance=extra_guidance),
        build_middleware = build_middleware(enable_hitl=use_hitl),
        response_format= ProviderStrategy(TurnSummary),
        name = "Coding Agent"
    )
