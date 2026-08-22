"""Toyota / regional dealer official news & press releases for the Supra family.

Scope (per the final spec — broader than a road-car-only draft): the road-going GR
Supra (A90/A91, MK5, 2019-) AND the racing derivatives, Supra GT4 (customer racing)
and Supra GT500 / GR Supra GT500 (SUPER GT). All three get their own name-variant
query sets, OR'd together and deduped, per the skill's query-design lesson: an
exact-phrase query for "GR Supra 3.0" will not match "GR Supra GT4" or "GRMN"-style
names, so each real name gets its own parallel query.
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency

# Global / North America trim & edition names (production road car).
_GLOBAL_TRIMS = [
    "GR Supra 3.0",
    "GR Supra 2.0",
    "GR Supra A91-MT Edition",
    "GR Supra 45th Anniversary Edition",
    "GR Supra A91-CF Edition",
]

# Japan-market trim names (Toyota Japan's GR Supra grade lineup).
_JP_TRIMS = ["GRスープラ RZ", "GRスープラ SZ-R", "GRスープラ SZ"]

# Racing derivatives — customer GT4 racer and the SUPER GT GT500 works car.
_RACING_NAMES_EN = ["Supra GT4", "GR Supra GT4", "Supra GT500", "GR Supra GT500"]
_RACING_NAMES_JP = ["スープラ GT4", "GRスープラ GT4", "スープラ GT500", "GRスープラ GT500"]

QUERIES = [
    # 北米(米国・カナダ)/ グローバル英語圏 — production
    *[(f'"{trim}" Toyota press release OR announcement', "en-US", "US", "US:en") for trim in _GLOBAL_TRIMS],
    *[(f'"{trim}" site:pressroom.toyota.com OR site:global.toyota', "en-US", "US", "US:en") for trim in _GLOBAL_TRIMS],
    ('"GR Supra" Toyota Canada press release OR announcement', "en-CA", "CA", "CA:en"),
    # 日本(トヨタ自動車 / GAZOO Racing / 各グレード) — production
    ("GRスープラ トヨタ 発表 OR 発売 OR 新型", "ja", "JP", "JP:ja"),
    *[(f'{trim} トヨタ 発表 OR 発売', "ja", "JP", "JP:ja") for trim in _JP_TRIMS],
    # 欧州 — production
    ('"GR Supra" Toyota Europe press release OR announcement', "en-GB", "GB", "GB:en"),
    ('"GR Supra" site:newsroom.toyota.eu OR site:toyota.eu', "en-GB", "GB", "GB:en"),
    # オセアニア(豪州・NZ) — production
    ('"GR Supra" Toyota Australia press release OR announcement', "en-AU", "AU", "AU:en"),
    ('"GR Supra" Toyota New Zealand press release OR announcement', "en-NZ", "NZ", "NZ:en"),
    # レーシング(GT4 / GT500) — グローバル・日本
    *[(f'"{name}" Toyota press release OR announcement OR homologation', "en-US", "US", "US:en") for name in _RACING_NAMES_EN],
    *[(f'{name} トヨタ 発表 OR ホモロゲーション OR 新型', "ja", "JP", "JP:ja") for name in _RACING_NAMES_JP],
    ('"Supra GT4" TOYOTA GAZOO Racing announcement', "en-US", "US", "US:en"),
    ("スープラ GT500 SUPER GT トヨタ 発表", "ja", "JP", "JP:ja"),
]


def fetch(limit_per_query: int = 8) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid in QUERIES:
        items.extend(fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query))
    return sort_by_recency(dedupe_by_url(items))
