from __future__ import annotations
import re
from .config import LANGUAGE_LABELS, TOPIC_CN, SCENE_RULES
from .client import ask_llm

def clean_text(text: str) -> str:
    return re.sub(r"\\s+", " ", (text or "").replace("\\n", " ")).strip()

def zh_language(language: str) -> str:
    return LANGUAGE_LABELS.get(language or "Unknown", language or "未识别")

def topic_cn(topic: str) -> str:
    return TOPIC_CN.get(topic, topic)

def topic_tags_cn(topics: list[str], limit: int = 4) -> str:
    if not topics:
        return "-"
    labels = [topic_cn(t) for t in topics[:limit]]
    return " / ".join(labels)

def infer_scene(item: dict) -> str:
    # Try LLM first
    topics = item.get("topics", [])
    desc = clean_text(item.get("description", ""))
    prompt = f"Based on the following project details, suggest a 1-sentence usage scenario in Chinese (e.g., '适合做 XXX'). Project: {item.get('full_name')}, Description: {desc}, Topics: {topics}. Return ONLY the sentence."
    
    ai_scene = ask_llm(prompt)
    if ai_scene:
        return ai_scene
        
    # Fallback to rules
    desc_lower = desc.lower()
    for keys, scene in SCENE_RULES:
        if any(k in topics for k in keys) or any(k in desc_lower for k in keys):
            return scene
    return "适合关注 AI 新项目、产品形态和工程实现思路"

def infer_kind(item: dict) -> str:
    topics = item.get("topics", [])
    if any(t in topics for t in ["ai-agent", "ai-agents", "agent", "agents", "multi-agent", "autonomous-agent"]):
        return "智能体项目"
    if any(t in topics for t in ["rag", "search", "mcp", "openapi", "graphql"]):
        return "搜索与工具接入项目"
    if any(t in topics for t in ["automation", "productivity", "cli", "developer-tools"]):
        return "自动化与效率工具项目"
    if any(t in topics for t in ["course", "interview", "awesome", "awesome-list"]):
        return "学习资料与资源聚合项目"
    return "AI 项目"

def summarize_project_cn(item: dict) -> str:
    # AI-powered summary
    full_name = item.get("full_name", "")
    desc = clean_text(item.get("description", ""))
    topics = topic_tags_cn(item.get("topics", []))
    language = zh_language(item.get("language", "Unknown"))
    
    prompt = (
        f"Project Name: {full_name}\n"
        f"Description: {desc}\n"
        f"Topics: {topics}\n"
        f"Language: {language}\n\n"
        "Task: Write a professional, concise one-sentence summary in Chinese. "
        "Focus on its core value and target audience. Avoid generic phrases like 'This project is...'. "
        "The output should be a natural sentence that describes what it does and who it is for."
    )
    
    ai_summary = ask_llm(prompt)
    if ai_summary:
        return ai_summary
        
    # Fallback to old logic if LLM fails
    lower_name = full_name.lower()
    desc_lower = desc.lower()
    
    # Simplified fallback mapping for brevity
    mapping = {
        "cloner": "用于借助 AI 快速克隆网页结构，适合作为网站复刻和前端原型生成的脚手架",
        "autoresearch": "用于让 Claude Code 按目标持续执行“修改、验证、保留或回退”的自动研究流程",
        "novel": "用于多智能体协作完成小说写作、审稿与修订",
        "mcp": "用于把 MCP/OpenAPI 能力快速转成命令行工具",
        "awesome": "用于整理和索引优质开源 AI 项目与基础设施",
    }
    
    core = "关注该方向的工程实践"
    for key, value in mapping.items():
        if key in lower_name or key in desc_lower:
            core = value
            break
            
    return f"这是一个{infer_kind(item)}，{core}。"

def simplify(item: dict) -> dict:
    return {
        "full_name": item["full_name"],
        "html_url": item["html_url"],
        "description": item.get("description") or "",
        "language": item.get("language") or "Unknown",
        "stargazers_count": item.get("stargazers_count", 0),
        "forks_count": item.get("forks_count", 0),
        "open_issues_count": item.get("open_issues_count", 0),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "topics": item.get("topics", []),
        "owner": item.get("owner", {}).get("login", ""),
    }
