import os
import argparse

from dotenv import load_dotenv
from smolagents import CodeAgent,LiteLLMModel,tool

from server import get_pr_diff as _get_pr_diff
from server import run_linter as _run_linter

load_dotenv()

@tool
def get_pr_diff(owner: str,repo: str,pr_number: int) -> dict:
    """
    Fetch the changed files and diff patches for a GitHub pull request.

    Args:
        owner: repository owner or org, e.g. "psf"
        repo: repository name, e.g. "requests"
        pr_number: the pull request number, e.g. 6432
    """

    return _get_pr_diff(owner,repo,pr_number)

@tool
def run_linter(code: str,filename: str = "snippet.py") -> dict:
    """
    Run the ruff Python linter on a code string and return structured issues.

    Args:
        code: the Python source code to lint
        filename: filename for context, e.g. "utils.py"
    """

    return _run_linter(code,filename)

def build_agent() -> CodeAgent:
    model = LiteLLMModel(
        model_id="groq/llama-3.3-70b-versatile",
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    return CodeAgent(tools=[get_pr_diff,run_linter],
                     model = model,
                     additional_authorized_imports=["json"],
                     )

def main():

    parser = argparse.ArgumentParser(description="Review a GitHub PR with an agent")
    parser.add_argument("--owner",required=True)
    parser.add_argument("--repo",required=True)
    parser.add_argument("--pr",required=True)

    args = parser.parse_args()

    agent = build_agent()

    task = (
        f"Review pull request #{args.pr} in {args.owner}/{args.repo}.\n"
        f"1. Call get_pr_diff to fetch the changed files.\n"
        f"2. For each changed python files, extract the new code from the patch and call run_linter on it"
        f"3. Summerize: for each file, list the linter issues found, then give a short overall verdict (good to merge / needs fixes) with reasoning."
    )

    result = agent.run(task)
    print("REVIEW RESULT")

    print(result)


if __name__ == "__main__":
    main()
