"""Section 3: news topics about the rival vehicles from the catalog (section 2).

Google News RSS per rival, grouped by rival key. Each rival gets both a "newest"
(recency-sorted) and a "popular" view — "popular" here is Google News' own
relevance-ranked order (the order results come back in before we re-sort), NOT an
engagement metric — there is no article-body access and therefore no real
engagement signal available. This is stated plainly in the UI note (see app.js).
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .rivals import RIVALS


def _fetch_rival(rival: dict, limit_per_query: int = 8) -> dict:
    items: list[dict] = []
    for rank_query_idx, (query, hl, gl, ceid) in enumerate(rival["news_queries"]):
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for rank, item in enumerate(results):
            # 元のRSS順(=Googleニュースの関連度順)を保持しておき、"popular"表示に使う。
            item["_rank"] = rank_query_idx * limit_per_query + rank
        items.extend(results)

    best: dict[str, dict] = {}
    for item in items:
        key = item.get("url") or item.get("title")
        if not key:
            continue
        if key not in best or item["_rank"] < best[key]["_rank"]:
            best[key] = item
    deduped = list(best.values())

    popular = sorted(deduped, key=lambda x: x["_rank"])
    newest = sort_by_recency(deduped)
    for item in deduped:
        item.pop("_rank", None)

    return {
        "key": rival["key"],
        "label": rival["label"],
        "newest": newest,
        "popular": popular,
    }


def fetch(limit_per_query: int = 8) -> list[dict]:
    return [_fetch_rival(rival, limit_per_query=limit_per_query) for rival in RIVALS]
