"""Shared rival-vehicle roster for sections 3 (topics) and 4 (YouTube).

Single source of truth for "which rival cars" so the news-topics module and the
YouTube module stay in sync on naming. This list intentionally mirrors (but is
independent of) the static hand-curated catalog in site/data/rivals.json (section 2)
— that JSON drives the spec/price card grid, this list drives live query fan-out.

Every entry gets its own exact-phrase query per the skill's query-design lesson
(searching "BMW M2" alone won't reliably distinguish from "BMW M240i" chatter, so
each nameplate is anchored with the manufacturer name and, where useful, a
disambiguating word).

`title_filter`: YouTube's search-results page (unlike Google News RSS) does loose
relevance matching even for a specific-looking query — confirmed in production when
a "フェアレディZ 試乗" query surfaced an unrelated "日産 ムラーノ" (Nissan Murano)
test-drive video with no "Z"/"フェアレディ" mention at all. `youtube.fetch()` uses
this list of case-insensitive regexes as a post-fetch guard: a result is kept only if
its title matches at least one pattern, dropped otherwise. Word-boundaries (`\b`) are
used so a bare model number like `m2` doesn't also match `m235i` or similar.
"""

from __future__ import annotations

RIVALS: list[dict] = [
    {
        "key": "porsche_911",
        "label": "Porsche 911",
        "news_queries": [
            ('"Porsche 911" Carrera review OR news', "en-US", "US", "US:en"),
            ("ポルシェ 911 カレラ ニュース OR 試乗", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ['"Porsche 911" Carrera 2026', 'ポルシェ "911" 試乗'],
        "title_filter": [r"\b911\b"],
    },
    {
        "key": "porsche_718_cayman",
        "label": "Porsche 718 Cayman",
        "news_queries": [
            ('"718 Cayman" Porsche news OR review OR production', "en-US", "US", "US:en"),
            ("ポルシェ 718 ケイマン ニュース OR 生産終了", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ['"Porsche 718 Cayman" review', 'ポルシェ "ケイマン"'],
        "title_filter": [r"\bcayman\b", r"ケイマン"],
    },
    {
        "key": "corvette_c8",
        "label": "Chevrolet Corvette",
        "news_queries": [
            ('"Chevrolet Corvette" OR "Corvette C8" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ['"Chevrolet Corvette" C8 review 2026'],
        "title_filter": [r"\bcorvette\b", r"コルベット"],
    },
    {
        "key": "camaro",
        "label": "Chevrolet Camaro",
        "news_queries": [
            ('"Chevrolet Camaro" news OR discontinued OR future', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ['"Chevrolet Camaro" 2026'],
        "title_filter": [r"\bcamaro\b", r"カマロ"],
    },
    {
        "key": "nissan_gtr",
        "label": "Nissan GT-R",
        "news_queries": [
            ('"Nissan GT-R" news OR production OR final edition', "en-US", "US", "US:en"),
            ("日産 GT-R ニュース OR 生産終了", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ['"Nissan GT-R" 2026', '日産 "GT-R"'],
        "title_filter": [r"\bgt-?r\b", r"\br35\b"],
    },
    {
        "key": "nissan_z",
        "label": "Nissan Z",
        "news_queries": [
            ('"Nissan Z" Performance news OR review', "en-US", "US", "US:en"),
            ("日産 フェアレディZ ニュース OR 試乗", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ['"Nissan Z" Performance review', '"フェアレディZ" 試乗'],
        # プレーンな "z" 単体は他の日産車(例: ムラーノ)のタイトルとも紛らわしい
        # 語句にマッチしうるため使わず、必ず"Nissan"や日本語の固有名詞と
        # セットになった語形のみを許可する。
        "title_filter": [r"\bnissan\s*z\b", r"フェアレディ", r"\brz34\b", r"\bz34\b"],
    },
    {
        "key": "bmw_m2",
        "label": "BMW M2",
        "news_queries": [
            ('"BMW M2" news OR review', "en-US", "US", "US:en"),
            ("BMW M2 ニュース OR 試乗", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ['"BMW M2" review 2026'],
        "title_filter": [r"\bm2\b"],
    },
    {
        "key": "bmw_m3",
        "label": "BMW M3",
        "news_queries": [
            ('"BMW M3" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ['"BMW M3" review 2026'],
        "title_filter": [r"\bm3\b"],
    },
    {
        "key": "bmw_m4",
        "label": "BMW M4",
        "news_queries": [
            ('"BMW M4" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ['"BMW M4" review 2026'],
        "title_filter": [r"\bm4\b"],
    },
    {
        "key": "mustang_dark_horse",
        "label": "Ford Mustang Dark Horse",
        "news_queries": [
            ('"Mustang Dark Horse" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ['"Ford Mustang Dark Horse" review'],
        "title_filter": [r"\bmustang\b", r"マスタング"],
    },
]
