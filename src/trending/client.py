from __future__ import annotations
import json
import urllib.parse
import urllib.request
from .config import API_URL, PER_PAGE

def github_get(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "daily-ai-growth-bot",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            raise RuntimeError(f"GitHub API returned HTTP {resp.status}")
        return json.loads(resp.read().decode("utf-8"))

def fetch_projects(token: str, query: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(PER_PAGE),
            "page": "1",
        }
    )
    url = f"{API_URL}?{params}"
    return github_get(url, token)
