"""Toyota / regional dealer official news & press releases for the Supra family.

Scope (per the final spec — broader than a road-car-only draft): the road-going GR
Supra (A90/A91, MK5, 2019-) AND the racing derivatives, Supra GT4 (customer racing)
and Supra GT500 / GR Supra GT500 (SUPER GT). All three get their own name-variant
query sets, OR'd together and deduped, per the skill's query-design lesson: an
exact-phrase query for "GR Supra 3.0" will not match "GR Supra GT4" or "GRMN"-style
names, so each real name gets its own parallel query.

**Restricted to official sources only** (verified live 2026-09-05): every query is
anchored with a `site:` filter (or an OR'd group of them) to Toyota's own regional
newsroom/pressroom domains — this section had been leaking third-party media
articles (blogs/outlets reporting *about* an announcement, which also happen to
contain words like "press release" or "発表" in their own headline/body) because
the previous query set searched those words unrestricted. A verified test query —
`"GR Supra 3.0" (site:pressroom.toyota.com OR site:media.toyota.ca OR
site:global.toyota OR site:newsroom.toyota.eu OR site:pressroom.toyota.com.au OR
site:toyota.co.nz)` — returned zero non-official results across ~20 items, all
attributed to pressroom.toyota.com / Newsroom Toyota Europe / トヨタ自動車株式会社
公式企業サイト. Google News RSS supports parenthesized multi-`site:` OR groups.

Verified official domains, one per region:
  - US: pressroom.toyota.com
  - Canada: media.toyota.ca
  - Global newsroom (also carries Japan-sourced global announcements in English):
    global.toyota
  - Europe: newsroom.toyota.eu
  - Australia: pressroom.toyota.com.au
  - New Zealand: toyota.co.nz (no separate pressroom subdomain found; the whole
    domain is Toyota NZ's own site)
  - Japan (Toyota Motor Corp itself, incl. the GR Garage dealer-network hub page
    toyota.jp/gr/garage/): toyota.jp
  - Racing (TOYOTA GAZOO Racing, GT4/GT500 press releases): toyotagazooracing.com

Japan's actual GR Supra dealer network ("販売会社") is dozens of independent
regional Toyota dealer corporations (トヨタモビリティ東京, 愛知トヨタ, Weins Toyota
神奈川, etc.), each on its own domain with no unifying pressroom — enumerating
them all isn't practical or maintainable. toyota.jp (which includes Toyota Japan's
own GR Garage hub page) is the closest thing to an official, stable anchor for
"Japan dealer network" coverage; genuinely dealer-specific stories are a known gap.
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

# 英語圏の公式ニュースルーム(米・加・欧・豪・NZ・グローバル)。OR結合して1クエリで検索する。
_OFFICIAL_SITES_EN = [
    "pressroom.toyota.com",
    "media.toyota.ca",
    "global.toyota",
    "newsroom.toyota.eu",
    "pressroom.toyota.com.au",
    "toyota.co.nz",
]
# レーシング(TOYOTA GAZOO Racing公式)は上記の英語圏ニュースルームにも重ねて配信される
# ことがあるため、両方をOR結合する。
_RACING_SITES_EN = ["toyotagazooracing.com"] + _OFFICIAL_SITES_EN


def _site_filter(domains: list[str]) -> str:
    return "(" + " OR ".join(f"site:{d}" for d in domains) + ")"


QUERIES = [
    # 北米/欧州/豪州/NZ/グローバル公式ニュースルーム — production(グレード別)
    *[(f'"{trim}" {_site_filter(_OFFICIAL_SITES_EN)}', "en-US", "US", "US:en") for trim in _GLOBAL_TRIMS],
    # 日本(トヨタ自動車公式サイト。GR Garage販売店網の公式ハブページもtoyota.jp配下)
    ("GRスープラ site:toyota.jp", "ja", "JP", "JP:ja"),
    *[(f"{trim} site:toyota.jp", "ja", "JP", "JP:ja") for trim in _JP_TRIMS],
    # レーシング(GT4 / GT500) — TOYOTA GAZOO Racing公式 + 英語圏公式ニュースルーム
    *[(f'"{name}" {_site_filter(_RACING_SITES_EN)}', "en-US", "US", "US:en") for name in _RACING_NAMES_EN],
    *[(f"{name} site:toyotagazooracing.com", "ja", "JP", "JP:ja") for name in _RACING_NAMES_JP],
]


def fetch(limit_per_query: int = 8) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid in QUERIES:
        items.extend(fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query))
    return sort_by_recency(dedupe_by_url(items))
