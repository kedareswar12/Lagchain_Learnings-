from dotenv import load_dotenv
from dataclasses import dataclass
import os

from langchain_groq.chat_models import ChatGroq 

load_dotenv()


@dataclass (frozen = True)
class Provider:
    name : str
    env_var : str
    base_url : str | None
    is_free : bool
    model : str

PROVIDERS = [
    Provider(
        name = "Groq",
        env_var = "GROQ_API_KEY",
        base_url = "https://api.groq.com/openai/v1",
        is_free = True ,
        model = "openai/gpt-oss-120b"

    )
]


def get_provider() -> Provider :
    for provider in PROVIDERS:
        if os.getenv(provider.env_var):
            return provider
    raise RuntimeError("No provider found") 

def build_chat_model (provider : Provider)-> [ChatGroq , Provider]:
    provider = get_provider()
    kwargs : dict  = {
        "model" : provider.model ,
        "api_key" : os.getenv(provider.env_var)
    }
    if provider.base_url is not None:
        kwargs["base_url"] = provider.base_url

    return ChatGroq(**kwargs), provider