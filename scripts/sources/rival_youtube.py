"""Section 4: YouTube videos about the rival vehicles from the catalog (section 2).

Same technique as youtube.py: one search-results fetch per query, sorted two ways
(view count for "popular", relative-time-parsed recency for "newest") rather than
two separate fetches. Grouped by rival key, same shape as rival_topics.py, so the
frontend can reuse one per-rival tab component for both sections.
"""

from __future__ import annotations

from . import youtube
from .rivals import RIVALS


def fetch(top_n: int = 12) -> list[dict]:
    results: list[dict] = []
    for rival in RIVALS:
        videos = youtube.fetch(
            queries=rival["youtube_queries"],
            top_n=top_n,
            hl="en",
            gl="US",
            require_any=rival.get("title_filter"),
        )
        results.append(
            {
                "key": rival["key"],
                "label": rival["label"],
                "newest": videos["new"],
                "popular": videos["popular"],
            }
        )
    return results
