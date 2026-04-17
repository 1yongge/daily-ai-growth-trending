from __future__ import annotations
import re
from .config import LANGUAGE_LABELS, TOPIC_CN, SCENE_RULES

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
    topics = item.get("topics", [])
    desc = clean_text(item.get("description", "")).lower()
    for keys, scene in SCENE_RULES:
        if any(k in topics for k in keys) or any(k in desc for k in keys):
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
    topics = item.get("topics", [])
    language = zh_language(item.get("language", "Unknown"))
    kind = infer_kind(item)
    scene = infer_scene(item)
    topic_text = topic_tags_cn(topics, limit=3)

    name = item.get("full_name", "该项目").split("/")[-1]
    lower_name = name.lower()
    desc = clean_text(item.get("description", ""))
    desc_lower = desc.lower()

    mapping = {
        "cloner": "用于借助 AI 快速克隆网页结构，适合作为网站复刻和前端原型生成的脚手架",
        "clone any website": "用于借助 AI 快速克隆网页结构，适合作为网站复刻和前端原型生成的脚手架",
        "autoresearch": "用于让 Claude Code 按目标持续执行“修改、验证、保留或回退”的自动研究流程",
        "karpathy": "用于让 Claude Code 按目标持续执行“修改、验证、保留或回退”的自动研究流程",
        "inkos": "用于多智能体协作完成小说写作、审稿与修订，强调人类审核关卡",
        "novel": "用于多智能体协作完成小说写作、审稿与修订，强调人类审核关卡",
        "mirofish": "用于离线运行多智能体模拟与预测任务，可结合 Neo4j 和 Ollama 进行本地部署",
        "simulation": "用于离线运行多智能体模拟与预测任务，可结合 Neo4j 和 Ollama 进行本地部署",
        "bookmarks": "用于对收藏内容做 AI 分类整理，并以思维导图方式辅助回顾与管理",
        "mindmap": "用于对收藏内容做 AI 分类整理，并以思维导图方式辅助回顾与管理",
        "mcp": "用于把 MCP、OpenAPI 或 GraphQL 能力快速转成命令行工具，便于接入自动化流程",
        "openapi": "用于把 MCP、OpenAPI 或 GraphQL 能力快速转成命令行工具，便于接入自动化流程",
        "graphql": "用于把 MCP、OpenAPI 或 GraphQL 能力快速转成命令行工具，便于接入自动化流程",
        "awesome": "用于整理和索引优质开源 AI 项目、模型、工具与基础设施",
        "interview": "用于系统整理 AI Engineering 面试问题与答案，适合准备面试和查漏补缺",
        "skills": "用于整理 Golang 方向的 agent skills，便于扩展 AI coding workflow",
        "golang": "用于整理 Golang 方向的 agent skills，便于扩展 AI coding workflow",
        "office": "用于让 AI agent 直接读写和自动化处理 Word、Excel、PowerPoint 文件",
        "hello-claw": "用于学习 OpenClaw 的 中文教程与实践路径，适合作为入门资料",
        "holyclaude": "用于搭建面向 AI 编程的工作台，整合 Claude Code、Web UI 与多种 CLI 工具",
        "architecture": "用于收集和展示大语言模型架构相关资料，方便做模型结构学习与查阅",
        "nightingale": "用于结合机器学习能力实现卡拉 OK 打分与演唱体验增强",
        "karaoke": "用于结合机器学习能力实现卡拉 OK 打分与演唱体验增强",
        "crucix": "用于持续监控多个信息源，在目标信息变化时主动通知用户，偏向个人情报跟踪",
        "osint": "用于持续监控多个信息源，在目标信息变化时主动通知用户，偏向个人情报跟踪",
        "intelligence": "用于持续监控多个信息源，在目标信息变化时主动通知用户，偏向个人情报跟踪",
        "search hub": "用于聚合多家 AI 搜索能力，统一接入趋势查询、热点追踪与信息检索",
        "ai-search-hub": "用于聚合多家 AI 搜索能力，统一接入趋势查询、热点追踪与信息检索",
    }

    core = "关注该方向的工程实践"
    for key, value in mapping.items():
        if key in lower_name or key in desc_lower:
            core = value
            break
    else:
        if desc:
            core = f"围绕“{topic_text}”展开，主要使用 {language} 实现，适合关注该方向的工程实践"
        else:
            core = f"围绕“{topic_text}”展开，主要使用 {language} 实现"

    return f"这是一个{kind}，{core}。{scene}。"

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
