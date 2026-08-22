"""FR Sports Car Watchダッシュボード用データを収集し、site/data/latest.jsonへ出力する。

30分おきにGitHub Actionsから実行される想定。site/data/rivals.json(ライバル車カタログ)は
別ファイルで、この本体JSONとは独立して手動キュレーションされている(fetch_data.pyでは
生成しない)。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

from sources import complaints, historic_youtube, inline_six, motorsports, official_news, rival_topics, rival_youtube, sentiment

JST = timezone(timedelta(hours=9))
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "latest.json"


def _with_sentiment(items: list[dict]) -> list[dict]:
    return sentiment.attach_sentiment(items)


def _rival_group_with_sentiment(rivals: list[dict]) -> list[dict]:
    for r in rivals:
        r["newest"] = _with_sentiment(r["newest"])
        r["popular"] = _with_sentiment(r["popular"])
    return rivals


def _motorsports_section() -> dict:
    regions = motorsports.fetch()
    for r in regions.values():
        for series in r["series"]:
            series["topics"] = _with_sentiment(series["topics"])
            series["results"] = _with_sentiment(series["results"])
            series["standings"] = _with_sentiment(series["standings"])
    return {"regions": regions}


def build_dashboard() -> dict:
    now_utc = datetime.now(timezone.utc)
    now_jst = now_utc.astimezone(JST)

    complaint_data = complaints.fetch()
    inline_six_data = inline_six.fetch()

    return {
        "generated_at_utc": now_utc.isoformat(),
        "generated_at_jst": now_jst.strftime("%Y-%m-%d %H:%M JST"),
        "sections": {
            "official_news": {
                "items": _with_sentiment(official_news.fetch()),
            },
            "rival_topics": {
                "rivals": _rival_group_with_sentiment(rival_topics.fetch()),
            },
            "rival_youtube": {
                "rivals": _rival_group_with_sentiment(rival_youtube.fetch()),
            },
            "historic_youtube": {
                "generations": _rival_group_with_sentiment(historic_youtube.fetch()),
            },
            "inline_six": {
                "newest": _with_sentiment(inline_six_data["newest"]),
                "popular": _with_sentiment(inline_six_data["popular"]),
            },
            "complaints": {
                "items_latest": _with_sentiment(complaint_data["items_latest"]),
                "items_buzz": _with_sentiment(complaint_data["items_buzz"]),
            },
            "motorsports": _motorsports_section(),
        },
    }


def main() -> None:
    dashboard = build_dashboard()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote dashboard data to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
