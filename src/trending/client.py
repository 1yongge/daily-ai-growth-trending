from __future__ import annotations
import json
import urllib.parse
import urllib.request
from .config import API_URL, PER_PAGE, LLM_API_URL, LLM_API_KEY, LLM_MODEL

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

def ask_llm(prompt: str) -> str:
    if not LLM_API_KEY:
        return ""
    
    data = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional AI technology analyst. Provide concise, high-quality summaries in Chinese."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
    }).encode("utf-8")

    req = urllib.request.Request(
        LLM_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"LLM API Error: {e}")
        return ""
