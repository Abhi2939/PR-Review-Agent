import os

from dotenv import load_dotenv
from smolagents import CodeAgent,LiteLLMModel,tool

from server import get_pr_diff
from server import run_linter

load_dotenv()

@tool
def get_pr_diff(owner: str,repo: str,pr_number: int) -> dict:

    return get_pr_diff(owner,repo,pr_number)

@tool
def run_linter(code: str,filename: str = "snippet.py") -> dict:

    return run_linter(code,filename)

def build_agent() -> CodeAgent:
    model = LiteLLMModel(
        model_id="groq/llama-3.3-70b-versatile",
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    return CodeAgent(tools=[get_pr_diff,run_linter],model = model)