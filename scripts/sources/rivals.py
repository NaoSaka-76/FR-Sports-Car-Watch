"""Shared rival-vehicle roster for sections 3 (topics) and 4 (YouTube).

Single source of truth for "which rival cars" so the news-topics module and the
YouTube module stay in sync on naming. This list intentionally mirrors (but is
independent of) the static hand-curated catalog in site/data/rivals.json (section 2)
— that JSON drives the spec/price card grid, this list drives live query fan-out.

Every entry gets its own exact-phrase query per the skill's query-design lesson
(searching "BMW M2" alone won't reliably distinguish from "BMW M240i" chatter, so
each nameplate is anchored with the manufacturer name and, where useful, a
disambiguating word).
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
        "youtube_queries": ["Porsche 911 Carrera 2026", "ポルシェ 911 試乗"],
    },
    {
        "key": "porsche_718_cayman",
        "label": "Porsche 718 Cayman",
        "news_queries": [
            ('"718 Cayman" Porsche news OR review OR production', "en-US", "US", "US:en"),
            ("ポルシェ 718 ケイマン ニュース OR 生産終了", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ["Porsche 718 Cayman review", "ポルシェ 718 ケイマン"],
    },
    {
        "key": "corvette_c8",
        "label": "Chevrolet Corvette",
        "news_queries": [
            ('"Chevrolet Corvette" OR "Corvette C8" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ["Chevrolet Corvette C8 review 2026"],
    },
    {
        "key": "camaro",
        "label": "Chevrolet Camaro",
        "news_queries": [
            ('"Chevrolet Camaro" news OR discontinued OR future', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ["Chevrolet Camaro 2026"],
    },
    {
        "key": "nissan_gtr",
        "label": "Nissan GT-R",
        "news_queries": [
            ('"Nissan GT-R" news OR production OR final edition', "en-US", "US", "US:en"),
            ("日産 GT-R ニュース OR 生産終了", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ["Nissan GT-R 2026", "日産 GT-R"],
    },
    {
        "key": "nissan_z",
        "label": "Nissan Z",
        "news_queries": [
            ('"Nissan Z" Performance news OR review', "en-US", "US", "US:en"),
            ("日産 フェアレディZ ニュース OR 試乗", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ["Nissan Z Performance review", "フェアレディZ 試乗"],
    },
    {
        "key": "bmw_m2",
        "label": "BMW M2",
        "news_queries": [
            ('"BMW M2" news OR review', "en-US", "US", "US:en"),
            ("BMW M2 ニュース OR 試乗", "ja", "JP", "JP:ja"),
        ],
        "youtube_queries": ["BMW M2 review 2026"],
    },
    {
        "key": "bmw_m3",
        "label": "BMW M3",
        "news_queries": [
            ('"BMW M3" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ["BMW M3 review 2026"],
    },
    {
        "key": "bmw_m4",
        "label": "BMW M4",
        "news_queries": [
            ('"BMW M4" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ["BMW M4 review 2026"],
    },
    {
        "key": "mustang_dark_horse",
        "label": "Ford Mustang Dark Horse",
        "news_queries": [
            ('"Mustang Dark Horse" news OR review', "en-US", "US", "US:en"),
        ],
        "youtube_queries": ["Ford Mustang Dark Horse review"],
    },
]
