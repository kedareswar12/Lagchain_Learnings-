# from dataclasses import dataclass
# from schemas import TurnSummary
# from typing import Any
# from langgraph.types import Command
# from messages import last_ai_text , last_tool_text
# from tools.text import prepare_file_content 

# class AgentTurnResult:
#     text: str #represents agents reply
#     structured: TurnSummary | None
#     messages: list[Any]
#     pending_interrupt: dict[str, Any] | None
    
# def parse_invoke_result(result: Any) -> AgentTurnResult:
#     interrupts = tuple(getattr(result, "interrupts", ()) or ())
#     # get the complete graph state using the value property
#     value = getattr(result, "value", result)
#     if not isinstance(value, dict):
#         value = {} 
    
#     messages = value.get("messages") or []

#     if interrupts:
#         payload = interrupts[0].value 
#         return AgentTurnResult(
#             text="",
#             structured=None,
#             messages=messages,
#             pending_interrupt=payload if isinstance(payload, dict) else {"raw": payload}
#         )
    
#     return AgentTurnResult(
#         text=last_ai_text(messages) or last_tool_text(messages),
#         structured=_as_summary(value.get("structured_response")),
#         messages=messages,
#         pending_interrupt=None
#     )

    
# def _as_summary(value: Any) -> TurnSummary | None:
#     if value is None:
#         return None 
#     if isinstance(value, TurnSummary):
#         return value 
#     if isinstance(value, dict):
#         try:
#             return TurnSummary.model_validate(value)
#         except Exception:
#             return None
#     return None


# def start_turn(agent, user_text: str, config: dict) -> AgentTurnResult:
#     result = agent.invoke(
#         {"messages": [{"role": "user", "content": user_text}]},
#         config=config,
#         version="v2"
#     )
#     return parse_invoke_result(result)


# def resume_turn(agent, decisions: list[dict], config: dict) -> AgentTurnResult:
#     result = agent.invoke(
#         Command(resume={
#             "decisions": decisions
#         }),
#         config=config,
#         version="v2"
#     )
#     return parse_invoke_result(result)
  
# def format_interrupt(pending: dict[str, Any]) -> str:
#     requests = pending.get("action_requests") or [] 
#     lines = []

#     for index, action in enumerate(requests, start=1):
#         name = action.get("name", "?")
#         args = dict(action.get("args") or {})
#         description = action.get("description", "?")
#         lines.append(f"{index}. {name} ({description})")
#         for key, value in args.items():
#             preview = str(value)
#             if key in {"content", "old_str", "new_str"}:
#                 preview = prepare_file_content(str(args.get("path") or ""), preview)
#             if "\n" in preview:
#                 lines.append(f"    {key}:")
#                 for body_line in preview.splitlines():
#                     lines.append(f"        {body_line}")
#                 continue 

#             if len(preview) > 240:
#                 preview = preview[:240] + "..."
#             lines.append(f"    {key}: {preview}")
#     return "\n".join(lines) if lines else str(pending)

from dataclasses import dataclass
from schemas import TurnSummary
from typing import Any
from langgraph.types import Command
from messages import last_ai_text, last_tool_text
from part2_coding_agent_mvp.tools.text import prepare_file_content
from models import build_chat_model


@dataclass
class AgentTurnResult:
    text: str  # represents agents reply
    structured: TurnSummary | None
    messages: list[Any]
    pending_interrupt: dict[str, Any] | None


def parse_invoke_result(result: Any) -> AgentTurnResult:
    interrupts = tuple(getattr(result, "interrupts", ()) or ())
    # get the complete graph state using the value property
    value = getattr(result, "value", result)
    if not isinstance(value, dict):
        value = {}

    messages = value.get("messages") or []

    if interrupts:
        payload = interrupts[0].value
        return AgentTurnResult(
            text="",
            structured=None,
            messages=messages,
            pending_interrupt=payload if isinstance(payload, dict) else {"raw": payload}
        )

    text = last_ai_text(messages) or last_tool_text(messages)

    return AgentTurnResult(
        text=text,
        structured=summarize_turn(text) if text else None,
        messages=messages,
        pending_interrupt=None
    )


def summarize_turn(text: str) -> TurnSummary | None:
    """
    Makes a separate, tools-free call to structure the agent's final
    text answer into a TurnSummary. Kept as a second call because Groq
    rejects response_format combined with tool/function calling on the
    main agent call.
    """
    if not text:
        return None

    model, _ = build_chat_model()
    structured_model = model.with_structured_output(TurnSummary)

    try:
        result = structured_model.invoke(
            f"Summarize the following assistant response into the required structure:\n\n{text}"
        )
    except Exception:
        return None

    return _as_summary(result)


def _as_summary(value: Any) -> TurnSummary | None:
    if value is None:
        return None
    if isinstance(value, TurnSummary):
        return value
    if isinstance(value, dict):
        try:
            return TurnSummary.model_validate(value)
        except Exception:
            return None
    return None


def start_turn(agent, user_text: str, config: dict) -> AgentTurnResult:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)


def resume_turn(agent, decisions: list[dict], config: dict) -> AgentTurnResult:
    result = agent.invoke(
        Command(resume={
            "decisions": decisions
        }),
        config=config,
        version="v2"
    )
    return parse_invoke_result(result)


def format_interrupt(pending: dict[str, Any]) -> str:
    requests = pending.get("action_requests") or []
    lines = []

    for index, action in enumerate(requests, start=1):
        name = action.get("name", "?")
        args = dict(action.get("args") or {})
        description = action.get("description", "?")
        lines.append(f"{index}. {name} ({description})")
        for key, value in args.items():
            preview = str(value)
            if key in {"content", "old_str", "new_str"}:
                preview = prepare_file_content(str(args.get("path") or ""), preview)
            if "\n" in preview:
                lines.append(f"    {key}:")
                for body_line in preview.splitlines():
                    lines.append(f"        {body_line}")
                continue

            if len(preview) > 240:
                preview = preview[:240] + "..."
            lines.append(f"    {key}: {preview}")
    return "\n".join(lines) if lines else str(pending)