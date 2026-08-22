"""Customer complaint / defect coverage for the road-going GR Supra (public news only).

Not connected to any internal CRM/complaint system. Aggregates publicly reported
recall/defect/complaint news via Google News RSS.
"""

from __future__ import annotations

from .common import fetch_google_news_rss, sort_by_recency

NEWS_QUERIES = [
    ('"GR Supra" recall OR complaint OR problem OR issue OR defect', "en-US", "US", "US:en"),
    ("GRスープラ 不具合 OR クレーム OR リコール", "ja", "JP", "JP:ja"),
    ('"GR Supra" recall OR complaint OR defect', "en-AU", "AU", "AU:en"),
]


def _dedupe_keep_best_rank(items: list[dict]) -> list[dict]:
    best: dict[str, dict] = {}
    for item in items:
        key = item.get("url") or item.get("title")
        if not key:
            continue
        if key not in best or item["_rank"] < best[key]["_rank"]:
            best[key] = item
    return list(best.values())


def fetch(limit_per_query: int = 10) -> dict:
    items: list[dict] = []
    for query, hl, gl, ceid in NEWS_QUERIES:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for rank, item in enumerate(results):
            item["_rank"] = rank
        items.extend(results)

    deduped = _dedupe_keep_best_rank(items)
    items_latest = sort_by_recency(deduped)
    items_buzz = sorted(deduped, key=lambda x: x["_rank"])
    for item in deduped:
        item.pop("_rank", None)

    return {
        "items_latest": items_latest,
        "items_buzz": items_buzz,
        "note": (
            "社内クレーム管理システムとは未連携です。ニュース報道(リコール等)で"
            "公開されている情報のみを集約した簡易モニタリングです。"
            "「話題順」は検索結果内での上位表示度を注目度の代替指標として用いています"
            "(実際のSNS拡散数やエンゲージメント数ではありません)。"
        ),
    }
