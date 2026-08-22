"""Series standings (real data) for the Supra motorsports series with static HTML.

Verified against live pages (2026-08-22):
  - SUPER GT GT500/GT300: https://supergt.net/en/driver_ranking (GT300 via
    ?gt_class=gt300, confirmed to genuinely filter — <span class="bib gt300">
    vs <span class="bib gt500"> in the returned rows).
  - Formula Drift Japan: https://formulad.jp/2026-fdj-standings/ (plain <table>,
    columns: Rank, Car(no.), Driver, Rd1..Rd8, Total, Behind, SW — "Total" column
    index is resolved from the header row text, not hardcoded, since column count
    can shift season to season).
  - D1GP: https://d1gp.co.jp/{2026-slug}/ — a Japanese URL-encoded slug found by
    browsing the site nav (not a stable-looking path, so it's read from a constant
    here rather than re-discovered every run; re-verify if this section goes empty).
  - Formula Drift (US) Pro: https://www.formulad.com/standings/2026/pro — IS real,
    server-rendered static HTML (re-verified 2026-08-22 with a browser User-Agent;
    an earlier pass without one apparently got a different/blocked response and
    wrongly concluded this was JS-only). Not a `<table>` — a div-based CSS grid
    (`<div class="standings-grid grid ..." role="row">`), so the parser here
    targets specific class strings instead of table/tr/td tags: the rank cell has
    class `text-xl lg:text-2xl...`, the driver name is inside
    `<span class="uppercase truncate">`, the car number follows as `#<!-- -->NNN`,
    and the season-total points cell is the one with class
    `text-base lg:text-lg py-2 pr-2 flex items-center justify-end` (distinct from
    the "points behind leader" cell that follows it, and from the header row's
    cells which lack the `text-xl lg:text-2xl` / `text-base lg:text-lg` size
    classes). Re-verify this class-name scheme if the section goes empty — it's a
    Next.js site and rebuilds can change generated class names.
  - Supercars Championship (Australia): https://www.supercars.com/standings/2026/supercars
    — re-verified 2026-08-23 with a browser User-Agent: real season standings ARE
    present, but as a genuine Next.js RSC "flight" payload (`self.__next_f.push([N,
    "<json-escaped string>"])`) rather than HTML markup at all — the driver list is a
    `"driverStats":[...]` JSON array double-encoded inside that pushed string. See
    `_extract_next_flight_array()` below for the two-step decode (parse the push()
    call as a JSON array literal, then bracket-match the named array out of the
    resulting string and json.loads it). This is a real internal implementation
    detail of the site's framework, not a documented API — it can break silently on
    a site rebuild if the chunk stops containing this key or the field names change;
    re-verify if this section goes empty. The `/schedule` page, by contrast, has no
    event data anywhere in its initial HTML/flight payload (checked directly) — it's
    fetched by client-side JS after hydration from an endpoint this project doesn't
    have visibility into, so schedule stays link-out only; only standings were fixed.

GR Supra / GR Supra GT500 entrants are flagged (`is_supra`) using a name list
gathered from official team/driver sourcing, not by string-matching "Supra" in the
row itself (SUPER GT rows don't list the car model at all — only the ranking site's
per-team pages do).
"""

from __future__ import annotations

import html as html_module
import json
import re

import requests

from .common import REQUEST_TIMEOUT, USER_AGENT

SUPER_GT_RANKING_URL = "https://supergt.net/en/driver_ranking"
FDJ_STANDINGS_URL = "https://formulad.jp/2026-fdj-standings/"
D1GP_STANDINGS_URL = (
    "https://d1gp.co.jp/2026d1%e3%82%b0%e3%83%a9%e3%83%b3%e3%83%97%e3%83%aa"
    "%e3%82%b7%e3%83%aa%e3%83%bc%e3%82%ba%e3%83%a9%e3%83%b3%e3%82%ad%e3%83%b3"
    "%e3%82%b0/"
)
FORMULA_DRIFT_PRO_STANDINGS_URL = "https://www.formulad.com/standings/2026/pro"
SUPERCARS_STANDINGS_URL = "https://www.supercars.com/standings/2026/supercars"

# GRスープラ(GT500)で参戦するワークスチームのドライバー名(公式発表ベース)。
_GT500_SUPRA_DRIVERS = {
    "sho tsuboi", "kenta yamashita",  # TOM'S
    "nirei fukuzumi", "kazuya oshima",  # TOM'S
    "yuji kunimoto", "yuhi sekiguchi",  # Cerumo
    "kazuya oshima", "sho tsuboi",
    "yuichi nakayama", "kohta kawaai",  # SARD
    "kenta yamashita",
}
# GT300クラスのGR Supra参戦チーム(例: Saitama Green Brave)のドライバー名。
_GT300_SUPRA_DRIVERS = {"hiroki yoshida", "seita nonaka"}
# D1GPでGR Supraを駆るドライバー(No.87 齋藤/齋藤太吾, No.90 手塚)。
_D1GP_SUPRA_CAR_NUMBERS = {"87", "90"}
# FDJでGR Supraを駆るドライバー(松山英樹/北斗, CUSCO Racing)。
_FDJ_SUPRA_DRIVER_NAME_FRAGMENTS = {"matsuyama"}
# Formula Drift(米国PROクラス)でGR Supraを駆るドライバー
# (Fredric Aasbo: Papadakis Racing Rockstar Energy Toyota GR Supra、
#  Simen Olsen: 同じくGR Supraで参戦)。
_FORMULA_DRIFT_PRO_SUPRA_DRIVER_NAME_FRAGMENTS = {"aasbo", "olsen"}
# Supercars ChampionshipでGen3 GR Supraを駆るドライバー
# (WAU Racing: #1 Chaz Mostert, #2 Ryan Wood)。
_SUPERCARS_SUPRA_DRIVER_NAME_FRAGMENTS = {"mostert", "ryan wood"}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _extract_next_flight_array(html_text: str, array_key: str) -> list | None:
    """Pull a named JSON array out of a Next.js RSC "flight" payload.

    The data isn't in the page's HTML markup — it's inside a
    `<script>self.__next_f.push([N, "<json-escaped string>"])</script>` chunk. The
    pushed string is itself a JSON-escaped blob containing a second, ordinary JSON
    array under `array_key` (e.g. `"driverStats":[...]`). Two-step decode:
      1. Locate the <script> tag whose raw (still-escaped) text contains
         `\"{array_key}\":[` and parse its `push([...])` call as a JSON array
         literal — this un-escapes the inner string in one pass.
      2. Within that now-plain-JSON string, bracket-match the array starting right
         after `"{array_key}":` (tracking string state so brackets inside quoted
         values don't confuse the depth count) and `json.loads` just that slice.
    Returns None if the key isn't found anywhere in the page.
    """
    needle = f'\\"{array_key}\\":['
    pos = html_text.find(needle)
    if pos == -1:
        return None

    script_start = html_text.rfind("<script", 0, pos)
    script_end = html_text.find("</script>", pos)
    script_content = html_text[script_start:script_end]

    push_idx = script_content.find("push([")
    if push_idx == -1:
        return None
    push_arg = script_content[push_idx + len("push(") :].rstrip()
    if push_arg.endswith(")"):
        push_arg = push_arg[:-1]
    outer = json.loads(push_arg)
    inner_text = outer[1] if len(outer) > 1 else outer[0]

    key_pos = inner_text.find(f'"{array_key}":[')
    if key_pos == -1:
        return None
    array_start = key_pos + len(f'"{array_key}":')

    depth = 0
    in_str = False
    escaped = False
    i = array_start
    while i < len(inner_text):
        ch = inner_text[i]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
                if depth == 0:
                    i += 1
                    break
        i += 1

    return json.loads(inner_text[array_start:i])


def fetch_super_gt_standings(clazz: str = "gt500", limit: int = 15) -> dict:
    session = _session()
    url = SUPER_GT_RANKING_URL + (f"?gt_class={clazz}" if clazz == "gt300" else "")
    supra_drivers = _GT500_SUPRA_DRIVERS if clazz == "gt500" else _GT300_SUPRA_DRIVERS
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        table_m = re.search(r'<table class="common driver_ranking".*?</table>', html_text, re.S)
        if not table_m:
            return {"standings": [], "error": "順位表の構造を特定できませんでした"}
        table_html = table_m.group(0)

        header_cells = re.findall(r"<th[^>]*>(.*?)</th>", table_html, re.S)
        header_labels = [_strip_tags(c) for c in header_cells]
        try:
            total_idx = header_labels.index("Total")
        except ValueError:
            total_idx = len(header_labels) - 3  # フォールバック(Behind/SWの手前)

        rows = re.findall(r"<tr>(.*?)</tr>", table_html, re.S)
        results: list[dict] = []
        for row in rows:
            if "<th" in row:
                continue
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if len(cells) < 3:
                continue
            position_text = _strip_tags(cells[0])
            if not position_text.isdigit():
                continue
            bib_m = re.search(r'class="bib[^"]*">([^<]*)<', cells[1])
            car_no = bib_m.group(1).strip() if bib_m else _strip_tags(cells[1])

            driver_names = re.findall(r'alt="([^"]+)"', cells[2])
            if not driver_names:
                driver_names = [_strip_tags(cells[2])]
            name = " / ".join(html_module.unescape(n) for n in driver_names)

            points_text = _strip_tags(cells[total_idx]) if total_idx < len(cells) else "0"
            points_text = re.sub(r"[^\d]", "", points_text) or "0"

            is_supra = any(n.lower() in supra_drivers for n in driver_names)
            results.append(
                {
                    "position": int(position_text),
                    "name": name,
                    "car": f"No.{car_no}",
                    "points": int(points_text),
                    "is_supra": is_supra,
                }
            )
            if len(results) >= limit:
                break

        return {
            "standings": results,
            "error": None if results else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_fdj_standings(limit: int = 15) -> dict:
    session = _session()
    try:
        resp = session.get(FDJ_STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        # ランキング本表(先頭のトップ3演出テーブルではなく、Rank/Car/Driver列を持つ表)を探す。
        tables = re.findall(r"<table[^>]*>.*?</table>", html_text, re.S)
        target_html = None
        for tbl in tables:
            if "Rank" in tbl and "Driver" in tbl:
                target_html = tbl
                break
        if not target_html:
            return {"standings": [], "error": "順位表の構造を特定できませんでした"}

        # ヘッダー行はRound列がcolspanで折り畳まれておりtd数が本体行と一致しないため、
        # ヘッダーテキストでの列特定は行わず、常に各行の最終セル(Total)を使う
        # (「231POINTS」のトップ3演出表示と突き合わせて実際に最終セル=Totalであることを確認済み)。
        rows = re.findall(r"<tr>(.*?)</tr>", target_html, re.S)
        results: list[dict] = []
        for row in rows[1:]:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if len(cells) < 4:
                continue
            position_text = _strip_tags(cells[0])
            if not position_text.isdigit():
                continue
            car_no = _strip_tags(cells[1])
            driver_cell = cells[2]
            name_links = re.findall(r">([^<]+)<", driver_cell)
            name = " ".join(n.strip() for n in name_links if n.strip())[:80]
            points_text = _strip_tags(cells[-1])
            points_text = re.sub(r"[^\d]", "", points_text) or "0"
            is_supra = any(frag in name.lower() for frag in _FDJ_SUPRA_DRIVER_NAME_FRAGMENTS)
            results.append(
                {
                    "position": int(position_text),
                    "name": name or f"#{car_no}",
                    "car": f"No.{car_no}",
                    "points": int(points_text),
                    "is_supra": is_supra,
                }
            )
            if len(results) >= limit:
                break

        return {
            "standings": results,
            "error": None if results else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_formula_drift_pro_standings(limit: int = 15) -> dict:
    session = _session()
    try:
        resp = session.get(FORMULA_DRIFT_PRO_STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        # div-based CSS grid, not a <table>: 1つの"row"は次の"standings-grid grid"
        # 出現位置までの区間として切り出す。
        rows = re.findall(
            r'<div class="standings-grid grid[^"]*"[^>]*role="row">.*?(?=<div class="standings-grid grid|\Z)',
            html_text,
            re.S,
        )
        results: list[dict] = []
        for row in rows:
            if 'role="columnheader"' in row:
                continue
            rank_m = re.search(r'<div role="cell" class="text-xl lg:text-2xl[^"]*"[^>]*>(\d+)</div>', row)
            name_m = re.search(r'<span class="uppercase truncate">([^<]+)</span>', row)
            if not rank_m or not name_m:
                continue
            car_m = re.search(r"#<!-- -->(\d+)", row)
            total_m = re.search(
                r'<div role="cell" class="text-base lg:text-lg py-2 pr-2 flex items-center justify-end"[^>]*>(-?\d+)</div>',
                row,
            )
            name = html_module.unescape(name_m.group(1)).strip()
            car_no = car_m.group(1) if car_m else "?"
            points = int(total_m.group(1)) if total_m else 0
            is_supra = any(frag in name.lower() for frag in _FORMULA_DRIFT_PRO_SUPRA_DRIVER_NAME_FRAGMENTS)
            results.append(
                {
                    "position": int(rank_m.group(1)),
                    "name": name,
                    "car": f"No.{car_no}",
                    "points": points,
                    "is_supra": is_supra,
                }
            )
            if len(results) >= limit:
                break

        return {
            "standings": results,
            "error": None if results else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_d1gp_standings(limit: int = 15) -> dict:
    session = _session()
    try:
        resp = session.get(D1GP_STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding or "utf-8"
        html_text = resp.text

        tables = re.findall(r"<table>\s*<thead>.*?</table>", html_text, re.S)
        target_html = None
        for tbl in tables:
            if "Driver" in tbl or "Rank" in tbl:
                target_html = tbl
                break
        if not target_html:
            return {"standings": [], "error": "順位表の構造を特定できませんでした"}

        header_row_m = re.search(r"<tr>(.*?)</tr>", target_html, re.S)
        header_cells = [_strip_tags(c) for c in re.findall(r"<th[^>]*>(.*?)</th>", header_row_m.group(1), re.S)] if header_row_m else []
        try:
            total_idx = header_cells.index("Total")
        except ValueError:
            total_idx = len(header_cells) - 1

        rows = re.findall(r"<tr>(.*?)</tr>", target_html, re.S)
        results: list[dict] = []
        for row in rows[1:]:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if len(cells) < 4:
                continue
            position_text = _strip_tags(cells[0])
            if not position_text.isdigit():
                continue
            car_no = _strip_tags(cells[1])
            name = html_module.unescape(_strip_tags(cells[2]))
            points_text = _strip_tags(cells[total_idx]) if total_idx < len(cells) else "0"
            points_text = re.sub(r"[^\d]", "", points_text) or "0"
            is_supra = car_no in _D1GP_SUPRA_CAR_NUMBERS
            results.append(
                {
                    "position": int(position_text),
                    "name": name,
                    "car": f"No.{car_no}",
                    "points": int(points_text) if points_text else 0,
                    "is_supra": is_supra,
                }
            )
            if len(results) >= limit:
                break

        return {
            "standings": results,
            "error": None if results else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}


def fetch_supercars_standings(limit: int = 15) -> dict:
    session = _session()
    try:
        resp = session.get(SUPERCARS_STANDINGS_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        html_text = resp.text

        driver_stats = _extract_next_flight_array(html_text, "driverStats")
        if not driver_stats:
            return {"standings": [], "error": "順位表の構造を特定できませんでした"}

        ranked = sorted(
            driver_stats,
            key=lambda d: d.get("totalSeasonPoints", 0),
            reverse=True,
        )
        results: list[dict] = []
        for position, d in enumerate(ranked, start=1):
            name = html_module.unescape(str(d.get("driverName", ""))).strip()
            if not name:
                continue
            car_no = str(d.get("driverNumber", "?"))
            points = int(d.get("totalSeasonPoints", 0) or 0)
            is_supra = any(frag in name.lower() for frag in _SUPERCARS_SUPRA_DRIVER_NAME_FRAGMENTS)
            results.append(
                {
                    "position": position,
                    "name": name,
                    "car": f"No.{car_no}",
                    "points": points,
                    "is_supra": is_supra,
                }
            )
            if len(results) >= limit:
                break

        return {
            "standings": results,
            "error": None if results else "現在、順位データが空です(シーズン開幕前などの可能性があります)",
        }
    except Exception as exc:  # noqa: BLE001
        return {"standings": [], "error": f"取得エラー: {exc}"}
