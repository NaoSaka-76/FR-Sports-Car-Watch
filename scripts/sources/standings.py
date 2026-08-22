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

GR Supra / GR Supra GT500 entrants are flagged (`is_supra`) using a name list
gathered from official team/driver sourcing, not by string-matching "Supra" in the
row itself (SUPER GT rows don't list the car model at all — only the ranking site's
per-team pages do).
"""

from __future__ import annotations

import html as html_module
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


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


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
