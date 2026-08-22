"""Motorsports where the GR Supra / Supra actually competes.

Scope: GT500, GT300, Formula Drift Japan, D1GP (Japan); Formula Drift Pro (US);
Supercars Championship (Australia). Grouped by region (REGIONS -> series list) per
the skill's nested shape.

Sources verified live on 2026-08-22 (see schedule.py / standings.py docstrings for
exact URLs and HTML structure snippets):
  - SUPER GT GT500/GT300, Formula Drift Japan, D1GP: static HTML, real schedule AND
    standings data scraped directly.
  - Formula Drift (US) Pro class: Fredric Aasbo (Papadakis Racing, Rockstar Energy
    Toyota GR Supra) and Simen Olsen race GR Supras. formulad.com does embed real
    schedule/standings data server-rendered, but inside a Next.js internal "flight"
    stream format with no stability guarantee (same risk class as the skill's ARA
    case study) rather than a documented HTML table — link-out only by design, not
    because the site is unreachable.
  - Supercars Championship (Australia): the Gen3-spec GR Supra joined the grid new
    for 2026 via Walkinshaw Andretti United — confirmed 2026 driver lineup is
    #1 Chaz Mostert and #2 Ryan Wood (WAU Racing), with Toyota fielding at least 4
    Gen3 Supras total across the field. supercars.com/schedule has no data in raw
    HTML (JS-rendered) and the standings page has the same Next.js flight-stream
    situation as Formula Drift US — both link-out only.
"""

from __future__ import annotations

import urllib.parse

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency
from .schedule import fetch_all_schedules
from .standings import fetch_d1gp_standings, fetch_fdj_standings, fetch_super_gt_standings


def _search_link(query: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote(query)


REGIONS = {
    "japan": {
        "label": "日本",
        "flag": "🇯🇵",
        "series": [
            {
                "key": "super_gt_gt500",
                "label": "SUPER GT GT500クラス",
                "queries": {
                    "topics": [
                        ('"GR Supra" "SUPER GT" GT500', "en-US", "US", "US:en"),
                        ("GRスープラ SUPER GT OR スーパーGT GT500", "ja", "JP", "JP:ja"),
                        ("SUPER GT GT500", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("GRスープラ SUPER GT GT500 決勝 OR レース結果 OR 表彰台 OR 優勝", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("SUPER GT GT500 ランキング OR ポイントランキング GRスープラ", "ja", "JP", "JP:ja"),
                    ],
                },
                "schedule_link": None,
                "standings_url": "https://supergt.net/en/driver_ranking",
            },
            {
                "key": "super_gt_gt300",
                "label": "SUPER GT GT300クラス(GR Supra参戦車両)",
                "queries": {
                    "topics": [
                        ('"GR Supra" "SUPER GT" GT300', "en-US", "US", "US:en"),
                        ("GRスープラ SUPER GT OR スーパーGT GT300", "ja", "JP", "JP:ja"),
                        ("SUPER GT GT300", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("GRスープラ SUPER GT GT300 決勝 OR レース結果 OR 表彰台", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("SUPER GT GT300 ランキング OR ポイントランキング GRスープラ", "ja", "JP", "JP:ja"),
                    ],
                },
                "schedule_link": None,
                "standings_url": "https://supergt.net/en/driver_ranking?gt_class=gt300",
            },
            {
                "key": "formula_drift_japan",
                "label": "Formula Drift Japan(FDJ)",
                "queries": {
                    "topics": [
                        ('"GR Supra" "Formula Drift Japan" OR FDJ', "en-US", "US", "US:en"),
                        ("GRスープラ フォーミュラドリフトジャパン OR FDJ", "ja", "JP", "JP:ja"),
                        ("フォーミュラドリフトジャパン OR \"Formula Drift Japan\"", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("GRスープラ FDJ 決勝 OR レース結果 OR 優勝 松山英樹 OR CUSCO", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("FDJ フォーミュラドリフトジャパン ランキング OR ポイントランキング", "ja", "JP", "JP:ja"),
                    ],
                },
                "schedule_link": None,
                "standings_url": "https://formulad.jp/2026-fdj-standings/",
            },
            {
                "key": "d1gp",
                "label": "D1GP",
                "queries": {
                    "topics": [
                        ('"GR Supra" D1GP OR "D1グランプリ"', "en-US", "US", "US:en"),
                        ("GRスープラ D1GP OR D1グランプリ 齋藤大貴 OR 手塚祥", "ja", "JP", "JP:ja"),
                        ("D1GP OR D1グランプリ", "ja", "JP", "JP:ja"),
                    ],
                    "results": [
                        ("GRスープラ D1GP 決勝 OR レース結果 OR 優勝 齋藤大貴 OR 手塚祥", "ja", "JP", "JP:ja"),
                    ],
                    "standings": [
                        ("D1GP D1グランプリ シリーズランキング OR ポイントランキング", "ja", "JP", "JP:ja"),
                    ],
                },
                "schedule_link": None,
                "standings_url": (
                    "https://d1gp.co.jp/2026d1%e3%82%b0%e3%83%a9%e3%83%b3%e3%83%97%e3%83%aa"
                    "%e3%82%b7%e3%83%aa%e3%83%bc%e3%82%ba%e3%83%a9%e3%83%b3%e3%82%ad%e3%83%b3%e3%82%b0/"
                ),
            },
        ],
    },
    "us": {
        "label": "米国",
        "flag": "🇺🇸",
        "series": [
            {
                "key": "formula_drift_pro",
                "label": "Formula Drift(PROクラス)",
                "queries": {
                    "topics": [
                        ('"GR Supra" "Formula Drift" Aasbo OR Olsen OR Papadakis', "en-US", "US", "US:en"),
                        ('"Formula Drift" PRO', "en-US", "US", "US:en"),
                    ],
                    "results": [
                        ('"GR Supra" "Formula Drift" race result OR podium OR win OR finish', "en-US", "US", "US:en"),
                    ],
                    "standings": [
                        ('"Formula Drift" PRO championship standings Toyota OR "GR Supra"', "en-US", "US", "US:en"),
                    ],
                },
                # formulad.com/schedule と /standings/2026/pro は実データを含むが、Next.jsの
                # 内部flight-stream形式(非公開・非文書化)に埋め込まれておりHTMLテーブルのような
                # 安定した構造ではないため、誤解析リスクを避け公式サイトへのリンクのみとする。
                "schedule_link": "https://www.formulad.com/schedule",
                "standings_url": "https://www.formulad.com/standings/2026/pro",
                "js_rendered_note": True,
            },
        ],
    },
    "australia": {
        "label": "オーストラリア",
        "flag": "🇦🇺",
        "series": [
            {
                "key": "supercars_championship",
                "label": "Supercars Championship(Gen3・GR Supra)",
                "queries": {
                    "topics": [
                        ('"GR Supra" Supercars Gen3 "Walkinshaw Andretti United"', "en-AU", "AU", "AU:en"),
                        ("Supercars Championship Gen3 Toyota", "en-AU", "AU", "AU:en"),
                        ('Supercars "Chaz Mostert" OR "Ryan Wood" GR Supra', "en-AU", "AU", "AU:en"),
                    ],
                    "results": [
                        ('"GR Supra" Supercars race result OR podium OR win', "en-AU", "AU", "AU:en"),
                    ],
                    "standings": [
                        ("Supercars Championship standings Toyota OR \"GR Supra\"", "en-AU", "AU", "AU:en"),
                    ],
                },
                # supercars.com/scheduleはJS描画で生HTMLにデータなし。standingsページは
                # 実データを含むがformulad.com同様Next.jsの内部flight-stream形式のため、
                # 誤解析リスクを避け両方とも公式サイトへのリンクのみとする。
                "schedule_link": "https://www.supercars.com/schedule",
                "standings_url": "https://www.supercars.com/standings/2026/supercars",
                "js_rendered_note": True,
            },
        ],
    },
}


def _fetch_group(query_list: list[tuple], limit: int = 5) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid in query_list:
        items.extend(fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit))
    return sort_by_recency(dedupe_by_url(items))


def _build_series(series_cfg: dict) -> dict:
    return {
        "key": series_cfg["key"],
        "label": series_cfg["label"],
        "topics": _fetch_group(series_cfg["queries"]["topics"]),
        "results": _fetch_group(series_cfg["queries"]["results"]),
        "standings": _fetch_group(series_cfg["queries"]["standings"]),
        "standings_url": series_cfg["standings_url"],
        "standings_chart": None,
        "standings_chart_note": None,
        "standings_error": False,
        "schedule": [],
        "schedule_link": series_cfg.get("schedule_link"),
    }


def fetch() -> dict:
    result: dict = {}
    for region_key, region in REGIONS.items():
        result[region_key] = {
            "label": region["label"],
            "flag": region["flag"],
            "series": [_build_series(s) for s in region["series"]],
        }

    schedules = fetch_all_schedules()

    for series in result["japan"]["series"]:
        if series["key"] in ("super_gt_gt500", "super_gt_gt300"):
            series["schedule"] = schedules.get("super_gt", [])
        elif series["key"] == "formula_drift_japan":
            series["schedule"] = schedules.get("formula_drift_japan", [])
        elif series["key"] == "d1gp":
            series["schedule"] = schedules.get("d1gp", [])

    gt500_chart = fetch_super_gt_standings(clazz="gt500")
    gt300_chart = fetch_super_gt_standings(clazz="gt300")
    fdj_chart = fetch_fdj_standings()
    d1gp_chart = fetch_d1gp_standings()

    for series in result["japan"]["series"]:
        if series["key"] == "super_gt_gt500":
            series["standings_chart"] = gt500_chart["standings"]
            series["standings_error"] = bool(gt500_chart["error"])
            series["standings_chart_note"] = (
                gt500_chart["error"]
                or "SUPER GT公式サイト(supergt.net)のGT500ドライバーズランキング実データ。"
                "GR Supraで参戦するワークスチーム(TOM'S・セルモ・SARD等)には目印を付けています。"
            )
        elif series["key"] == "super_gt_gt300":
            series["standings_chart"] = gt300_chart["standings"]
            series["standings_error"] = bool(gt300_chart["error"])
            series["standings_chart_note"] = (
                gt300_chart["error"]
                or "SUPER GT公式サイトのGT300クラス実データ(?gt_class=gt300で絞り込み)。"
                "GR Supra参戦チーム(Saitama Green Brave等)には目印を付けています。"
            )
        elif series["key"] == "formula_drift_japan":
            series["standings_chart"] = fdj_chart["standings"]
            series["standings_error"] = bool(fdj_chart["error"])
            series["standings_chart_note"] = (
                fdj_chart["error"]
                or "Formula Drift Japan公式サイト(formulad.jp)のランキング実データ。"
                "CUSCO Racing(松山英樹)等、GR Supraで参戦するドライバーには目印を付けています。"
            )
        elif series["key"] == "d1gp":
            series["standings_chart"] = d1gp_chart["standings"]
            series["standings_error"] = bool(d1gp_chart["error"])
            series["standings_chart_note"] = (
                d1gp_chart["error"]
                or "D1GP公式サイト(d1gp.co.jp)のシリーズランキング実データ。"
                "齋藤(FAT FIVE RACING #87)・手塚(WEINS Toyota神奈川 #90)等、GR Supraで参戦する"
                "ドライバーには目印を付けています。"
            )

    default_note = (
        "この公式サイトはサーバー側で描画されていますが、Next.jsの内部flight-stream形式という"
        "非公開・非文書化のデータ埋め込み方式のため、HTMLテーブルのような安定した構造での解析が"
        "できません。誤表示リスクを避けグラフ化・一覧化は行わず、公式サイトへのリンクのみとしています。"
    )
    for region in result.values():
        for series in region["series"]:
            if series["standings_chart_note"] is None:
                series["standings_chart_note"] = default_note

    return result
