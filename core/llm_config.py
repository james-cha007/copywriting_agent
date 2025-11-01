import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment")


def get_llm_model(model_name: str = "gpt-4o", temperature: float = 0.8):
    """Factory for LLM models. Keep config centralized so you can swap models easily."""
    return ChatOpenAI(
        model=model_name,
        openai_api_key=OPENAI_API_KEY,
        temperature=temperature,
    )