"""Section 6: worldwide inline-six / straight-six engine technology topics.

NOT Supra-specific. Covers inline-6 engine technology and models across all
manufacturers — Toyota's own new turbo I6, BMW B58, Mercedes-AMG M256, Mazda's
inline-6 (e-Skyactiv X/D, CX-60/CX-90), Nissan VR30DDTT, Jaguar Ingenium I6,
Hyundai/Genesis Smartstream I6, etc. The Supra's own 2JZ/B58-derived engine is one
thread among these, not the focus — it gets one query, not a dominant share.

Per the skill's query-design lesson, queries are anchored to specific engine-family
names plus "inline-six"/"straight-six"/"直列6気筒" phrasing rather than generic
single-word queries (which leak unrelated noise).
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency

QUERIES = [
    # ジャンル全体(直6/インライン6全般)
    ('"inline-six" OR "inline six" OR "straight-six" engine news', "en-US", "US", "US:en"),
    ("直列6気筒 エンジン ニュース OR 新型", "ja", "JP", "JP:ja"),
    # BMW B58
    ('BMW "B58" inline-six engine', "en-US", "US", "US:en"),
    ("BMW B58型 直列6気筒", "ja", "JP", "JP:ja"),
    # Mercedes-AMG M256
    ('Mercedes-AMG "M256" inline-six', "en-US", "US", "US:en"),
    # Mazda inline-6 (e-Skyactiv X/D, CX-60/CX-90)
    ('Mazda "inline-six" OR "e-Skyactiv" CX-60 OR CX-90', "en-US", "US", "US:en"),
    ("マツダ 直列6気筒 OR e-Skyactiv CX-60 OR CX-90", "ja", "JP", "JP:ja"),
    # Nissan VR30DDTT
    ('Nissan "VR30DDTT" OR "VR30" inline-six engine', "en-US", "US", "US:en"),
    # Jaguar Ingenium I6
    ('Jaguar Land Rover "Ingenium" inline-six', "en-US", "US", "US:en"),
    # Hyundai/Genesis Smartstream I6
    ('Genesis OR Hyundai "Smartstream" inline-six OR "straight-six"', "en-US", "US", "US:en"),
    # Toyota's new turbo inline-six
    ('Toyota new turbo "inline-six" engine', "en-US", "US", "US:en"),
    ("トヨタ 新型 直列6気筒 ターボ エンジン", "ja", "JP", "JP:ja"),
    # Supraの2JZ/B58由来エンジン(この中の一トピックとして)
    ('Supra "2JZ" OR "B58" engine technology', "en-US", "US", "US:en"),
]


def fetch(limit_per_query: int = 6) -> dict:
    items: list[dict] = []
    for query, hl, gl, ceid in QUERIES:
        results = fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query)
        for rank, item in enumerate(results):
            item["_rank"] = rank
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
        "newest": newest,
        "popular": popular,
        "note": (
            "Supra専用のセクションではなく、直列6気筒(インライン6)エンジンの技術動向を"
            "全メーカー横断で集約しています。「話題順」はGoogleニュース検索結果内での"
            "表示順(関連度順)を代替指標として用いたものです(実際のエンゲージメント数ではありません)。"
        ),
    }
