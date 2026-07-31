import os 

from fastmcp import FastMCP
from dotenv import load_dotenv
import requests

load_dotenv()

mcp = FastMCP("PR-Review-mcp")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"

def _gh_headers():
    headers = {"Accept":"application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

@mcp.tool()
def get_pr_diff(owner: str, repo: str, pr_number: int) -> dict:

    pr_url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
    files_url = f"{pr_url}/files"

    pr_resp = requests.get(pr_url,headers=_gh_headers(),timeout=15)
    pr_resp.raise_for_status()
    pr_data = pr_resp.json()

    files_resp = requests.get(files_url,headers=_gh_headers(),timeout=15)
    files_resp.raise_for_status()
    files_data = files_resp.json()


