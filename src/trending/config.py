from __future__ import annotations
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
README = ROOT / "README.md"

# Search Settings
SEARCH_DAYS = int(os.environ.get("SEARCH_DAYS", "30"))
TOP_N = int(os.environ.get("TOP_N", "20"))
PER_PAGE = min(max(TOP_N, 100), 100)
API_URL = "https://api.github.com/search/repositories"
GROWTH_WINDOW_DAYS = 30

# LLM Settings
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_API_URL = os.environ.get("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")

# Mapping Tables (Still kept as fallback)
LANGUAGE_LABELS = {
    "JavaScript": "JavaScript", "TypeScript": "TypeScript", "Python": "Python",
    "Go": "Go", "Rust": "Rust", "Shell": "Shell", "Swift": "Swift",
    "C": "C", "C#": "C#", "Dockerfile": "Dockerfile", "Markdown": "Markdown",
    "Unknown": "未识别",
}

TOPIC_CN = {
    "ai": "人工智能", "agents": "智能体", "agent": "智能体", "ai-agent": "AI 智能体",
    "ai-agents": "AI 智能体", "llm": "大语言模型", "llms": "大语言模型",
    "rag": "检索增强生成", "mcp": "MCP", "openapi": "OpenAPI", "graphql": "GraphQL",
    "automation": "自动化", "productivity": "效率工具", "nextjs": "Next.js",
    "typescript": "TypeScript", "python": "Python", "open-source": "开源",
    "skills": "技能系统", "assistant": "助手", "claude": "Claude",
    "claude-code": "Claude Code", "openclaw": "OpenClaw", "ollama": "Ollama",
    "offline": "离线", "multi-agent": "多智能体", "local-first": "本地优先",
    "cli": "命令行", "bookmarks": "书签管理", "search": "搜索",
    "osint": "开源情报", "intelligence": "情报分析", "categorization": "分类整理",
    "mindmap": "思维导图", "boilerplate": "脚手架", "generative-ai": "生成式 AI",
    "artificial-intelligence": "人工智能", "autonomous-agent": "自治智能体",
    "autoresearch": "自动研究", "iteration": "迭代执行", "coding-agent": "编程智能体",
    "api-wrapper": "API 封装", "macos": "macOS", "course": "课程",
    "interview": "面试", "developer-tools": "开发者工具", "template": "模板",
    "reverse-engineering": "逆向分析", "web-scraping": "网页抓取",
    "novel-generation": "小说生成", "creative-writing-ai": "AI 写作",
    "karaoke": "卡拉 OK", "karaoke-application": "卡拉 OK 应用",
    "bevy-engine": "Bevy 引擎", "demucs": "音频分离", "neo4j": "Neo4j",
    "cheap": "低成本",
}

SCENE_RULES = [
    (["ai-agent", "ai-agents", "agent", "agents", "multi-agent", "autonomous-agent"], "适合做 AI 智能体、自动执行和多 Agent 协作"),
    (["rag", "search", "openapi", "graphql", "mcp"], "适合做搜索增强、知识接入和工具编排"),
    (["automation", "productivity", "cli", "developer-tools"], "适合做自动化流程、命令行工具和研发提效"),
    (["course", "interview", "awesome", "awesome-list"], "适合做学习资料、知识梳理和入门参考"),
    (["bookmarks", "mindmap", "categorization"], "适合做信息整理、内容归档和个人知识管理"),
    (["coding-agent", "claude-code", "template", "boilerplate"], "适合做 AI 编程、项目脚手架和开发工作台"),
    (["offline", "local-first", "ollama"], "适合做本地部署、离线运行和私有化使用"),
]
