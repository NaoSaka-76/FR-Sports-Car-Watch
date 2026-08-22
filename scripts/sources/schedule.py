"""Race schedules for the Supra motorsports series that publish static HTML.

Verified against live pages (2026-08-22) with curl before writing these parsers:
  - SUPER GT (GT500/GT300 share one calendar): https://supergt.net/en/calendar
  - Formula Drift Japan (Pro class only, not FDJ2/FDJ3): https://formulad.jp/race/2026/
  - D1GP: https://d1gp.co.jp/23674/

Formula Drift (US) and Supercars Championship (Australia) are intentionally NOT
scraped here even though their pages turn out to be server-rendered: the schedule/
standings data on both sites is embedded inside a Next.js "flight" stream
(`self.__next_f.push(...)`), an internal, undocumented serialization format that can
change between Next.js versions without notice. This is the same category of risk the
skill's ARA case study warns about (an unofficial site's backing JSON with no format
guarantee) — regexing a documented HTML table is very different from regexing a
framework-internal wire format. Both are link-out only; see motorsports.py.
"""

from __future__ import annotations

import html as html_module
import re
from datetime import date

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

SUPER_GT_CALENDAR_URL = "https://supergt.net/en/calendar"
FDJ_SCHEDULE_URL = "https://formulad.jp/race/2026/"
D1GP_SCHEDULE_URL = "https://d1gp.co.jp/23674/"

_EN_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _status(sort_key: int) -> str:
    today_key = date.today().year * 10000 + date.today().month * 100 + date.today().day
    return "upcoming" if sort_key >= today_key else "completed"


def fetch_super_gt_schedule() -> list[dict]:
    """SUPER GT公式カレンダー(GT500/GT300共通)。<div class="schedule_date_s">の
    numerator_s(月)/denominator_s(日、レンジの場合は開始日のみ使用)から日付を組み立てる。"""
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(SUPER_GT_CALENDAR_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        row_re = re.compile(
            r'<span class="numerator_s">(\d+)</span>.*?<span class="denominator_s">([\d\-]+)</span>'
            r'.*?<a href="([^"]*)">([^<]*)</a>.*?<td>\s*([^<]*?)\s*</td>\s*<td>([^<]*)</td>',
            re.S,
        )
        for m in row_re.finditer(html_text):
            month_s, day_s, link, round_name, circuit, race_title = m.groups()
            year_m = re.search(r"(\d{4})", race_title)
            year = int(year_m.group(1)) if year_m else date.today().year
            start_day = int(day_s.split("-")[0])
            month = int(month_s)
            sort_key = year * 10000 + month * 100 + start_day
            events.append(
                {
                    "round": html_module.unescape(round_name.strip()),
                    "track": html_module.unescape(re.sub(r"\s+", " ", circuit).strip()),
                    "name": html_module.unescape(race_title.strip()),
                    "date_range": f"{year}.{month:02d}.{start_day:02d}",
                    "status": _status(sort_key),
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    for e in events:
        del e["sort_key"]
    return events


def fetch_formula_drift_japan_schedule() -> list[dict]:
    """Formula Drift Japan公式サイトの"2026 FD JAPAN SCHEDULE"リボン直下のみを対象とする
    (FDJ2/FDJ3は下位カテゴリーのため対象外)。"""
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(FDJ_SCHEDULE_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        ribbon_m = re.search(r'<h3 class="ribbon">(\d{4}) FD JAPAN SCHEDULE</h3>', html_text)
        if not ribbon_m:
            return []
        year = int(ribbon_m.group(1))
        start = ribbon_m.end()
        next_ribbon_m = re.search(r'<h3 class="ribbon">', html_text[start:])
        end = start + next_ribbon_m.start() if next_ribbon_m else len(html_text)
        block = html_text[start:end]

        row_re = re.compile(
            r'<div class="sche-txt">\s*Rd\.(\d+)\s+([^,<]+),\s*([^<]+?)<br\s*/>\s*'
            r'([A-Za-z]+)\s+(\d{1,2})(?:-(\d{1,2}))?\s*</div>',
            re.S,
        )
        for m in row_re.finditer(block):
            rd, track, pref, month_name, start_day, end_day = m.groups()
            month = _EN_MONTHS.get(month_name.strip().lower(), 0)
            sort_key = year * 10000 + month * 100 + int(start_day)
            date_range = f"{month_name} {start_day}"
            if end_day:
                date_range += f"-{end_day}"
            date_range += f", {year}"
            events.append(
                {
                    "round": f"Rd.{rd}",
                    "track": html_module.unescape(f"{track.strip()}, {pref.strip()}"),
                    "name": "",
                    "date_range": date_range,
                    "status": _status(sort_key),
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    for e in events:
        del e["sort_key"]
    return events


def fetch_d1gp_schedule() -> list[dict]:
    """D1GP公式サイトの年間開催スケジュール表(最初の<table>のみ、D1 EXHIBITIONは対象外)。"""
    session = _session()
    events: list[dict] = []
    try:
        resp = session.get(D1GP_SCHEDULE_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        year_m = re.search(r"(\d{4})年", html_text[:2000])
        year = int(year_m.group(1)) if year_m else date.today().year

        table_m = re.search(r"<table><thead>.*?</table>", html_text, re.S)
        if not table_m:
            return []
        table_html = table_m.group(0)
        rows = re.findall(r"<tr>(.*?)</tr>", table_html, re.S)
        for row in rows[1:]:  # skip header row
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            cells = [re.sub(r"<[^>]+>", "", html_module.unescape(c)).strip() for c in cells]
            if len(cells) < 3:
                continue
            round_name, date_text, track = cells[0], cells[1], cells[2]
            date_m = re.search(r"(\d{1,2})月(\d{1,2})日", date_text)
            if not date_m:
                continue
            month, start_day = int(date_m.group(1)), int(date_m.group(2))
            sort_key = year * 10000 + month * 100 + start_day
            events.append(
                {
                    "round": round_name,
                    "track": track,
                    "name": "",
                    "date_range": date_text,
                    "status": _status(sort_key),
                    "sort_key": sort_key,
                }
            )
    except Exception:  # noqa: BLE001
        return []

    events.sort(key=lambda e: e["sort_key"])
    for e in events:
        del e["sort_key"]
    return events


def fetch_all_schedules() -> dict:
    return {
        "super_gt": fetch_super_gt_schedule(),
        "formula_drift_japan": fetch_formula_drift_japan_schedule(),
        "d1gp": fetch_d1gp_schedule(),
    }
