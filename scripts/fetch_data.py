"""FR Sports Car Watchダッシュボード用データを収集し、site/data/latest.jsonへ出力する。

30分おきにGitHub Actionsから実行される想定。site/data/rivals.json(ライバル車カタログ)は
別ファイルで、この本体JSONとは独立して手動キュレーションされている(fetch_data.pyでは
生成しない)。

見出しの日本語訳(title_ja)はscripts/.translation_cache.jsonにURL単位でキャッシュする。
このワークフローはcontents:readのみでリポジトリへコミットバックしないため、このキャッシュ
ファイル自体はGitHub Actionsのactions/cache(run_id込みのユニークキー+prefix restore-keys)
で実行間を永続化する想定(.github/workflows/update-dashboard.yml参照)。ローカル実行時は
このファイルがそのまま蓄積される。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

from sources import complaints, historic_youtube, inline_six, motorsports, official_news, rival_topics, rival_youtube, sentiment, translate

JST = timezone(timedelta(hours=9))
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "site" / "data" / "latest.json"
TRANSLATION_CACHE_PATH = Path(__file__).resolve().parent / ".translation_cache.json"

_translation_cache: dict[str, str] = {}


def _load_translation_cache() -> dict[str, str]:
    if TRANSLATION_CACHE_PATH.exists():
        try:
            return json.loads(TRANSLATION_CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}
    return {}


def _save_translation_cache(cache: dict[str, str]) -> None:
    TRANSLATION_CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )


def _attach_translations(items: list[dict]) -> list[dict]:
    for item in items:
        title = item.get("title", "")
        url = item.get("url", "")
        if not url or not translate.needs_translation(title):
            continue
        cached = _translation_cache.get(url)
        if cached:
            item["title_ja"] = cached
            continue
        translated = translate.translate_to_ja(title)
        if translated:
            item["title_ja"] = translated
            _translation_cache[url] = translated
    return items


def _with_sentiment(items: list[dict]) -> list[dict]:
    return _attach_translations(sentiment.attach_sentiment(items))


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
    global _translation_cache
    _translation_cache = _load_translation_cache()
    cache_size_before = len(_translation_cache)

    dashboard = build_dashboard()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote dashboard data to {OUTPUT_PATH}")

    _save_translation_cache(_translation_cache)
    print(
        f"Translation cache: {cache_size_before} -> {len(_translation_cache)} entries "
        f"({len(_translation_cache) - cache_size_before} newly translated)"
    )


if __name__ == "__main__":
    main()
