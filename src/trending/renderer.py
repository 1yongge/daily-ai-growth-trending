from __future__ import annotations
from .processor import zh_language, topic_tags_cn, summarize_project_cn, infer_scene

def render_top3_card(idx: int, item: dict) -> list[str]:
    medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(idx, '⭐')
    zh_desc = summarize_project_cn(item)
    topics = topic_tags_cn(item.get('topics', []), limit=4)
    language = zh_language(item['language'])
    updated = (item['updated_at'] or '')[:10]
    scene = infer_scene(item)
    growth = item.get('growth', 0)
    return [
        f"### {medal} Top {idx} · [{item['full_name']}]({item['html_url']})",
        "",
        f"**本月涨星**: +{growth} | **总星数**: {item['stargazers_count']} | **Language**: {language} | **Updated**: {updated}",
        "",
        f"**项目简介**：{zh_desc}",
        "",
        f"**适用场景**：{scene}",
        "",
        f"**标签**：{topics}",
        "",
    ]

def render_readme(snapshot: dict, items: list[dict]) -> str:
    fetched_at = snapshot["fetched_at_shanghai"]
    query = snapshot["query"]
    lines = [
        "# Daily AI Growth Trending",
        "",
        "> 每天 09:00（Asia/Shanghai）自动更新 GitHub AI 项目【上涨速度】榜单。",
        "",
        "<p align=\"center\">",
        "  <img alt=\"banner\" src=\"https://img.shields.io/badge/GitHub-AI%20Growth-green?style=for-the-badge&logo=github\">",
        "  <img alt=\"schedule\" src=\"https://img.shields.io/badge/Update-Daily%2009%3A00-blue?style=for-the-badge\">",
        "  <img alt=\"timezone\" src=\"https://img.shields.io/badge/Timezone-Asia%2FShanghai-16a34a?style=for-the-badge\">",
        "</p>",
        "",
        "## Dashboard",
        "",
        "| 更新时间 | 榜单数量 | 查询范围 |",
        "|---|---:|---|",
        f"| `{fetched_at}` | **{len(items)}** | `{query}` |",
        "",
        "> [!NOTE]",
        "> 本榜单通过对比每日快照，计算最近 30 天的星标增长数量 ($\Delta Stars$) 进行排序，旨在发现处于【快速爆发期】的新项目。",
        "",
        "## Top 3 Growth Highlights",
        "",
    ]

    for idx, item in enumerate(items[:3], start=1):
        lines.extend(render_top3_card(idx, item))

    lines.extend([
        "## Top 20 Growth Overview",
        "",
        "| # | Project | Growth | Total Stars | Language | 项目简介 | Updated |",
        "|---:|---|---:|---:|---|---|---|",
    ])

    for idx, item in enumerate(items, start=1):
        updated = (item["updated_at"] or "")[:10]
        summary = summarize_project_cn(item)
        growth = item.get('growth', 0)
        if len(summary) > 36:
            summary = summary[:36] + "…"
        lines.append(
            f"| {idx} | [{item['full_name']}]({item['html_url']}) | 📈 +{growth} | ⭐ {item['stargazers_count']} | {zh_language(item['language'])} | {summary} | {updated} |"
        )

    lines.extend([
        "",
        "## Project Details",
        "",
    ])

    for idx, item in enumerate(items, start=1):
        zh_desc = summarize_project_cn(item)
        created = (item["created_at"] or "")[:10]
        updated = (item["updated_at"] or "")[:10]
        topics_cn = topic_tags_cn(item.get("topics", []), limit=6)
        scene = infer_scene(item)
        growth = item.get('growth', 0)
        lines.extend([
            "<details>",
            f"<summary><strong>{idx}. {item['full_name']}</strong> · 📈 +{growth} · ⭐ {item['stargazers_count']} · {zh_language(item['language'])}</summary>",
            "",
            f"- **Repository**: {item['html_url']}",
            f"- **Owner**: `{item['owner']}`",
            f"- **Created**: `{created}`",
            f"- **Updated**: `{updated}`",
            f"- **Topics**: {topics_cn}",
            f"- **项目简介**: {zh_desc}",
            f"- **适用场景**: {scene}",
            "",
            "</details>",
            "",
        ])

    lines.extend([
        "## Data Files",
        "",
        "- `data/latest.json`：最新快照",
        "- `data/YYYY-MM-DD.json`：每日归档",
        "",
        "## Workflow",
        "",
        "- Schedule: `0 1 * * *`",
        "- Timezone: `Asia/Shanghai`",
        "- Trigger: GitHub Actions",
        "",
        "## Local Run",
        "",
        "```bash",
        "export GITHUB_TOKEN=***",
        "python3 -m trending.main",
        "```",
        "",
        "## Query",
        "",
        "```text",
        "",
        "```",
        "",
    ])
    return "\n".join(lines)
