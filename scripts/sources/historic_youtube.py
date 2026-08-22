"""Section 5: historic Supra YouTube coverage, every generation, 1978-present.

Generations (verified chassis codes / years / colloquial Mk names):
  - A40/A50  Celica Supra / Celica XX      ~1978-1981   "Mk1"
  - A60      Celica Supra                  ~1981-1986   "Mk2"
  - A70      Supra (MA70)                  ~1986-1993   "Mk3"
  - A80      Supra (JZA80, 2JZ-GTE)        ~1993-2002   "Mk4" (most culturally
             iconic generation — Fast & Furious, tuner-culture staple)
  - A90/A91  GR Supra                      2019-present "Mk5"

Each generation gets its own parallel query set (chassis code + colloquial Mk name +
JP and EN terms), merged and deduped per generation — same per-variant-query-and-merge
technique used elsewhere in this skill. Both a newest/popular(view count) toggle AND a
generation filter are exposed by returning one block per generation (the frontend
builds the generation tabs from this shape) rather than one flat merged list.
"""

from __future__ import annotations

from . import youtube

GENERATIONS: list[dict] = [
    {
        "key": "a40_a50",
        "label": "A40/A50 (Celica Supra / Celica XX, 1978-1981)",
        "queries": [
            "Celica Supra A40 review",
            "Celica XX A50",
            "セリカXX A40",
            "セリカスープラ 旧車",
        ],
    },
    {
        "key": "a60",
        "label": "A60 (Celica Supra, 1981-1986)",
        "queries": [
            "Celica Supra A60 Mk2",
            "Toyota Celica Supra 1985",
            "セリカXX A60",
        ],
    },
    {
        "key": "a70",
        "label": "A70 (MA70 Supra, 1986-1993, Mk3)",
        "queries": [
            "Toyota Supra MA70 Mk3",
            "Supra A70 turbo review",
            "スープラ A70 MA70",
        ],
    },
    {
        "key": "a80",
        "label": "A80 (JZA80 Supra, 1993-2002, Mk4, 2JZ-GTE)",
        "queries": [
            "Toyota Supra JZA80 Mk4",
            "Supra A80 2JZ-GTE",
            "スープラ JZA80 2JZ",
            "スープラ A80 タービン",
        ],
    },
    {
        "key": "a90_a91",
        "label": "A90/A91 (GR Supra, 2019-present, Mk5)",
        "queries": [
            "GR Supra A90 review",
            "Toyota GR Supra Mk5",
            "GRスープラ A90",
        ],
    },
]


def fetch(top_n: int = 15) -> list[dict]:
    results: list[dict] = []
    for gen in GENERATIONS:
        videos = youtube.fetch(queries=gen["queries"], top_n=top_n, hl="en", gl="US")
        results.append(
            {
                "key": gen["key"],
                "label": gen["label"],
                "newest": videos["new"],
                "popular": videos["popular"],
            }
        )
    return results
