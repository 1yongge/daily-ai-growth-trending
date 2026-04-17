from __future__ import annotations
import datetime as dt
import json
import os
import sys
import pathlib
from .config import ROOT, DATA_DIR, README, SEARCH_DAYS, TOP_N, GROWTH_WINDOW_DAYS
from .client import fetch_projects
from .processor import simplify

def build_query() -> str:
    today = dt.datetime.now(dt.timezone.utc).date()
    created_after = today - dt.timedelta(days=SEARCH_DAYS)
    return f"topic:ai archived:false is:public created:>={created_after.isoformat()} stars:>10"

def get_historical_stars(full_name: str, days_ago: int) -> int | None:
    target_date = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=days_ago)).isoformat()
    history_file = DATA_DIR / f"{target_date}.json"
    if not history_file.exists():
        return None
    
    try:
        data = json.loads(history_file.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            if item["full_name"] == full_name:
                return item.get("stargazers_count", 0)
    except Exception:
        return None
    return None

def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is required", file=sys.stderr)
        return 1

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    query = build_query()
    try:
        payload = fetch_projects(token, query)
    except Exception as e:
        print(f"Error fetching projects: {e}", file=sys.stderr)
        return 1

    # 1. Simplify and fetch current stars
    current_items = [simplify(item) for item in payload.get("items", [])]
    
    # 2. Calculate Growth
    processed_items = []
    for item in current_items:
        full_name = item["full_name"]
        current_stars = item["stargazers_count"]
        
        # Try to find stars from GROWTH_WINDOW_DAYS ago
        old_stars = get_historical_stars(full_name, GROWTH_WINDOW_DAYS)
        
        if old_stars is not None:
            growth = current_stars - old_stars
        else:
            # Fallback: If no history, growth = stars since creation if created < 30d, else 0
            created_date = dt.date.fromisoformat(item["created_at"][:10])
            today = dt.datetime.now(dt.timezone.utc).date()
            if (today - created_date).days <= GROWTH_WINDOW_DAYS:
                growth = current_stars
            else:
                growth = 0 # New projects not in history and older than 30d have unknown growth
        
        item["growth"] = growth
        processed_items.append(item)

    # 3. Sort by Growth (Descending)
    processed_items.sort(key=lambda x: x["growth"], reverse=True)
    top_items = processed_items[:TOP_N]

    # 4. Snapshot and Save
    now_utc = dt.datetime.now(dt.timezone.utc)
    now_shanghai = now_utc.astimezone(dt.timezone(dt.timedelta(hours=8)))
    snapshot = {
        "fetched_at_utc": now_utc.isoformat(),
        "fetched_at_shanghai": now_shanghai.strftime("%Y-%m-%d %H:%M:%S UTC+8"),
        "query": query,
        "total_count": payload.get("total_count", 0),
        "top_n": TOP_N,
        "items": processed_items, # Save ALL for future growth calculations
    }

    archive_file = DATA_DIR / f"{now_shanghai.date().isoformat()}.json"
    latest_file = DATA_DIR / "latest.json"

    archive_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_file.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    
    from .renderer import render_readme
    README.write_text(render_readme(snapshot, top_items), encoding="utf-8")

    print(f"Wrote {archive_file}")
    print(f"Wrote {latest_file}")
    print(f"Updated {README}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
