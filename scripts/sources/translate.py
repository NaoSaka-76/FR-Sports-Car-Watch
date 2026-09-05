"""Keyless machine translation of non-Japanese headlines into Japanese.

Uses Google Translate's public web-frontend endpoint
(translate.googleapis.com/translate_a/single) — the same technique the popular
`googletrans` Python library relies on. No API key, no account, matching this
project's "no official API keys" design philosophy (see the AutomotiveResearch
skill's SKILL.md). This is an unofficial, undocumented endpoint: Google could
change its response shape or start blocking requests without notice, the same
risk class as the YouTube search-page scraping and Google News RSS techniques
already used elsewhere in this project — if this section goes empty/stops
working, re-verify the endpoint and response shape before assuming the titles
themselves are the problem.

Only titles that appear to contain no Japanese characters are translated (a
simple Unicode-range check covering hiragana/katakana/CJK ideographs), so
already-Japanese headlines are left untouched and never spend a request.
Callers are expected to cache results by a stable key (e.g. the item's URL)
across the 30-minute runs — see fetch_data.py — since this endpoint has no
documented rate limit and repeatedly re-translating unchanged headlines every
run would be wasteful and more likely to trigger throttling.
"""

from __future__ import annotations

import re

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

_JAPANESE_RE = re.compile(r"[぀-ヿ㐀-䶿一-鿿]")
_ENDPOINT = "https://translate.googleapis.com/translate_a/single"


def needs_translation(title: str) -> bool:
    """タイトルに日本語(ひらがな/カタカナ/漢字)が一切含まれていない場合のみ翻訳対象とする。"""
    return bool(title) and not _JAPANESE_RE.search(title)


def translate_to_ja(title: str) -> str | None:
    """タイトル全体を日本語に翻訳する。失敗時はNoneを返す(呼び出し側は元タイトルのみ表示)。"""
    try:
        resp = requests.get(
            _ENDPOINT,
            params={"client": "gtx", "sl": "auto", "tl": "ja", "dt": "t", "q": title},
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        chunks = data[0] if data and isinstance(data[0], list) else []
        translated = "".join(chunk[0] for chunk in chunks if chunk and chunk[0])
        return translated or None
    except Exception:  # noqa: BLE001
        return None
