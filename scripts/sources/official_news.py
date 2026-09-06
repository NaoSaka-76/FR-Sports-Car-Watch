"""Toyota / regional dealer official news & press releases for the Supra family.

Scope (per the final spec — broader than a road-car-only draft): the road-going GR
Supra (A90/A91, MK5, 2019-) AND the racing derivatives, Supra GT4 (customer racing)
and Supra GT500 / GR Supra GT500 (SUPER GT). All three get their own name-variant
query sets, OR'd together and deduped, per the skill's query-design lesson: an
exact-phrase query for "GR Supra 3.0" will not match "GR Supra GT4" or "GRMN"-style
names, so each real name gets its own parallel query.

**Restricted to official sources only** (verified live 2026-09-05): every query is
anchored with a `site:` filter (or an OR'd group of them) to Toyota's own regional
newsroom/pressroom domains — this section had been leaking third-party media
articles (blogs/outlets reporting *about* an announcement, which also happen to
contain words like "press release" or "発表" in their own headline/body) because
the previous query set searched those words unrestricted. A verified test query —
`"GR Supra 3.0" (site:pressroom.toyota.com OR site:media.toyota.ca OR
site:global.toyota OR site:newsroom.toyota.eu OR site:pressroom.toyota.com.au OR
site:toyota.co.nz)` — returned zero non-official results across ~20 items, all
attributed to pressroom.toyota.com / Newsroom Toyota Europe / トヨタ自動車株式会社
公式企業サイト. Google News RSS supports parenthesized multi-`site:` OR groups.

Verified official domains, one per region:
  - US: pressroom.toyota.com
  - Canada: media.toyota.ca
  - Global newsroom (also carries Japan-sourced global announcements in English):
    global.toyota
  - Europe: newsroom.toyota.eu
  - Australia: pressroom.toyota.com.au
  - New Zealand: toyota.co.nz (no separate pressroom subdomain found; the whole
    domain is Toyota NZ's own site)
  - Japan (Toyota Motor Corp itself, incl. the GR Garage dealer-network hub page
    toyota.jp/gr/garage/): toyota.jp
  - Racing (TOYOTA GAZOO Racing, GT4/GT500 press releases): toyotagazooracing.com

Japan's actual GR Supra dealer network ("販売会社") is dozens of independent
regional Toyota dealer corporations (トヨタモビリティ東京, 愛知トヨタ, Weins Toyota
神奈川, etc.), each on its own domain with no unifying pressroom. toyota.jp
(which includes Toyota Japan's own GR Garage hub page) is the closest thing to
an official, stable anchor for "Japan dealer network" coverage generally, and
a representative set of individual dealer-corporation domains is now also
queried directly (added 2026-09-06, see below) — enumerating all ~60+ dealer
corporations remains impractical, so this is a representative sample, not
exhaustive coverage.

**Added 2026-09-06 — worldwide distributor + Japan dealer expansion** (additive
only; every domain below was verified live via `curl`/WebFetch and via a direct
Google News RSS `site:` query returning genuine on-topic official content,
never third-party media, before being added):

*European national distributor pressrooms* (in addition to the pan-European
newsroom.toyota.eu already covered) — confirmed GR Supra is sold in these
markets with a distinct, actively-publishing national press site of its own:
  - UK: media.toyota.co.uk ("Toyota Media Site" — dated press releases,
    confirmed GR Supra + Toyota Gazoo Racing content)
  - Germany: toyota-media.de ("Toyota Deutschland Media-Website" — has its own
    RSS feeds incl. a dedicated motorsport.rss)
  - Italy: newsroom.toyota.it ("Newsroom Toyota Italia" — separate subdomain
    from the commercial toyota.it, confirmed GR Supra content)
  - Spain: prensa.toyota.es ("Sala de Prensa Toyota España" — the single
    richest of the four: extensive GR Supra road-car AND GT4 / GR Cup Spain
    racing coverage)
  These four need their own localized hl/gl/ceid per query (verified: querying
  them with an en-US locale returns zero results even when the domain clearly
  has matching content — Google News RSS gates results by locale, not just by
  the `site:` filter).

*Markets researched and explicitly NOT added* (either no genuine official news
indexing, or the vehicle isn't actually sold there via that channel):
  - South Africa (toyota.co.za), UAE (toyota.ae), Singapore (toyota.com.sg):
    GR Supra genuinely is/was sold in all three, but a direct Google News RSS
    `site:` probe on each returned only generic commercial/merchandise/service
    pages (T-shirts, servicing packages, lease offers) — no indexed press-release
    content to query against. Adding them would either return nothing useful or,
    worse, flood results with non-news marketing pages.
  - South Korea (toyota.co.kr / toyotakoreaapp.co.kr): GR Supra had a one-time
    30-unit limited launch in Jan 2020; the only indexed content is generic
    account/service notices, no vehicle press content.
  - France (toyota.fr / media.toyota.fr), Netherlands, Norway, Sweden, Poland:
    either redundant with newsroom.toyota.eu (France's results were the same
    "Newsroom Toyota Europe" articles) or indexed only generic used-car/product
    pages, not press content.
  - GT4/GT500 racing series-adjacent press channels (SRO, Super GT, customer
    team sites like TOM'S/SARD): no additional official (Toyota-operated, not
    third-party team) channel found beyond toyotagazooracing.com — team sites
    are independent race teams, not Toyota itself, and were deliberately not
    added to avoid diluting "official" to include commercial racing outfits.

*Japan dealer-corporation domains* (representative sample, GR Garage-network
priority; each verified via a Google News RSS `site:` probe combined with a
GR Supra / GR Corolla term to confirm real, on-topic indexed content — not
just a shop-locator page with no news):
  - トヨタモビリティ東京: toyota-mobi-tokyo.co.jp
  - 愛知トヨタ: aichi-toyota.jp
  - Weins Toyota神奈川: weins-toyota-kanagawa.co.jp
  - トヨタモビリティ中京: tm-chukyo.co.jp
  - 広島トヨタ: hiroshima-toyota.co.jp
  - 大阪トヨペット (GR Garage 大阪箕面 ほか): osaka-toyopet.jp
  - 群馬トヨタ (GR Garage 高崎IC ほか — richest content of the set: dated,
    per-model "一部改良"/抽選販売 blog posts): gtoyota.com
  - ネッツトヨタ兵庫 (GR Garage 神戸垂水): netzhyogo.jp
  - ネッツトヨタ東埼玉 (GR Garage さいたま中央): mynetz.jp
  - トヨタカローラ福岡 (dedicated GR Garage 福岡空港 site with its own NEWS
    section): grgarage-fukuoka.net
  - AGHトヨタ札幌 (dedicated GR Garage 札幌西 site, Hokkaido — also has its own
    NEWS section): gr-garage-sad.com

**Added 2026-09-06 (second pass) — TMNA/TME corporate-domain check + South America /
China / Thailand / South Africa research** (same standard as above: every domain
below was verified reachable and confirmed via a live Google News RSS `site:` probe
returning genuine, on-topic, dated GR Supra/racing content before being added):

*TMNA / TME corporate domains — checked, confirmed already covered, nothing added*:
Toyota Motor North America (TMNA, the Plano-TX entity for US sales/marketing/
manufacturing) publishes its own corporate press releases — executive changes,
annual sales results, manufacturing announcements — directly on pressroom.toyota.com
under its "Corporate" topic (e.g. "Toyota Motor North America Announces Executive
Change", "Toyota Motor North America Reports 2025 U.S. Sales Results"). No distinct
`tmna.com`-style domain exists; pressroom.toyota.com already IS TMNA's official
newsroom. Toyota Motor Europe (TME) is the same: its own corporate news publishes
directly on newsroom.toyota.eu's "Corporate" category
(newsroom.toyota.eu/corporate-news/, e.g. "Toyota Motor Europe announces executive
changes"). No separate TME-only domain found. Both are already fully covered by
domains already in this file — nothing added for either.

*South Africa (toyota.co.za) — ADDED, reversing the earlier rejection above*: GR
Supra and Supra GT4 (raced via the SA GR Cup one-make series) are both confirmed
officially sold/raced in South Africa (Toyota South Africa Motors / TSAM). No
dedicated media/press subdomain (e.g. a `media.toyota.co.za`) was found to exist —
toyota.co.za is TSAM's only site. The earlier rejection above used a generic locale
and found only commercial pages; re-probing with the country-correct locale
(hl=en-ZA, gl=ZA, ceid=ZA:en) surfaced genuine, dated, on-topic editorial content
credited to "Toyota South Africa" — e.g. "TOYOTA GR COROLLA GETS 8-SPEED AUTOMATIC",
"Driven: The new GR Corolla", "Toyota Launches GR Supra GT4 EVO2 for 2025 Season",
"Like a pro – GR Supra" — spanning dated articles from 2019 through 2025. Same
locale lesson already learned for the EU distributors applies here too: `site:`
alone was not sufficient with the wrong locale. GT500 was checked too
(`"Supra GT500" site:toyota.co.za`) and correctly returns zero — South Africa
doesn't run SUPER GT — so reusing the shared racing-name filter carries no
false-positive risk.

*Argentina — researched and rejected*: GR Supra had a genuine limited 10-unit
official launch in Argentina via GR Garage dealers, and Toyota Argentina has both a
main site (toyota.com.ar, with a "/descubri/newsroom" section) and a distinct media
subdomain (media.toyota.com.ar). A direct Google News RSS `site:` probe against both
domains (es-AR and es-419 locale variants, gl=AR) returned no genuine GR Supra
content at all — only one unrelated generic "Argentina en números" stats page. Not
added: the distributor exists and the vehicle was sold, but there's no indexed press
content to query against, same category as the South Africa/UAE/Singapore
rejections above (unlike South Africa, retrying Argentina's locale did not surface
anything — this is a genuine no-content case, not a locale bug).

*China (toyota.com.cn) — researched and rejected*: TOYOTA SUPRA was officially
launched in China in Nov 2020 via the FAW Toyota / GAC Toyota joint-venture retail
network, under Toyota (China) Investment Co.'s own corporate site toyota.com.cn,
which runs a genuine, actively-publishing media center (confirmed: dated articles
2003-2026, recall notices, PDF press-release downloads, and real hits for other GR
models — "TOYOTA GR86正式发布上市", "进化版GR YARIS将引进中国市场" — so this is a real
newsroom, not a commercial-only page). But neither the exact phrase "TOYOTA SUPRA"
nor the bare word "SUPRA" returns any genuinely on-topic indexed result for this
vehicle specifically (zh-CN/CN/CN:zh-Hans locale) — the bare-word probe returns only
tangential motorsport-commentary and dealer-network pages, the exact-phrase probe
returns zero. Not added: the model is sold and the domain is a real newsroom, but
Supra-specific content isn't indexed there in a way Google News RSS can retrieve.

*Thailand (toyota.co.th) — researched and rejected*: Toyota Motor Thailand does
officially sell GR Supra (confirmed: toyota.co.th/model/grsupra with current
pricing) and publishes ข่าวประชาสัมพันธ์ ("press release") content on its own main
site (toyota.co.th/news — no separate press subdomain exists, same "whole domain is
the local distributor's own site" situation as New Zealand above). But
`site:toyota.co.th` probes for `"GR Supra"` across three locale variants (th/TH/
TH:th and en/TH/TH:en) returned only generic catalogue/model/promotion pages (Camry,
Hilux, Alphard, GR86, etc.) — no on-topic GR Supra press content indexed. Not added.
"""

from __future__ import annotations

from .common import dedupe_by_url, fetch_google_news_rss, sort_by_recency

# Global / North America trim & edition names (production road car).
_GLOBAL_TRIMS = [
    "GR Supra 3.0",
    "GR Supra 2.0",
    "GR Supra A91-MT Edition",
    "GR Supra 45th Anniversary Edition",
    "GR Supra A91-CF Edition",
]

# Japan-market trim names (Toyota Japan's GR Supra grade lineup).
_JP_TRIMS = ["GRスープラ RZ", "GRスープラ SZ-R", "GRスープラ SZ"]

# Racing derivatives — customer GT4 racer and the SUPER GT GT500 works car.
_RACING_NAMES_EN = ["Supra GT4", "GR Supra GT4", "Supra GT500", "GR Supra GT500"]
_RACING_NAMES_JP = ["スープラ GT4", "GRスープラ GT4", "スープラ GT500", "GRスープラ GT500"]

# 英語圏の公式ニュースルーム(米・加・欧・豪・NZ・グローバル)。OR結合して1クエリで検索する。
_OFFICIAL_SITES_EN = [
    "pressroom.toyota.com",
    "media.toyota.ca",
    "global.toyota",
    "newsroom.toyota.eu",
    "pressroom.toyota.com.au",
    "toyota.co.nz",
]
# レーシング(TOYOTA GAZOO Racing公式)は上記の英語圏ニュースルームにも重ねて配信される
# ことがあるため、両方をOR結合する。
_RACING_SITES_EN = ["toyotagazooracing.com"] + _OFFICIAL_SITES_EN

# 欧州各国の公式販売代理店ニュースルーム(2026-09-06追加)。newsroom.toyota.eu(汎欧州)
# とは別に、各国ごとに独自運営されており実際にGR Supraの記事が確認できたもののみ。
# Google News RSSはhl/gl/ceidをその国のロケールに合わせないと検索結果が0件になる
# (site:フィルタだけでは足りない)ため、国ごとに個別クエリを持つ。
_EU_DISTRIBUTOR_SITES: dict[str, tuple[str, str, str, str]] = {
    # country_code: (domain, hl, gl, ceid)
    "GB": ("media.toyota.co.uk", "en-GB", "GB", "GB:en"),
    "DE": ("toyota-media.de", "de", "DE", "DE:de"),
    "IT": ("newsroom.toyota.it", "it", "IT", "IT:it"),
    "ES": ("prensa.toyota.es", "es", "ES", "ES:es"),
}

# 日本の販売会社(GR Garage網を中心とした代表サンプル、2026-09-06追加)。
# 単一の統一プレスルームが存在しないため、共有の販売会社サイト群を1つのOR
# グループとして持ち、車名クエリと組み合わせて使う。
_JP_DEALER_SITES = [
    "toyota-mobi-tokyo.co.jp",
    "aichi-toyota.jp",
    "weins-toyota-kanagawa.co.jp",
    "tm-chukyo.co.jp",
    "hiroshima-toyota.co.jp",
    "osaka-toyopet.jp",
    "gtoyota.com",
    "netzhyogo.jp",
    "mynetz.jp",
    "grgarage-fukuoka.net",
    "gr-garage-sad.com",
]


def _site_filter(domains: list[str]) -> str:
    return "(" + " OR ".join(f"site:{d}" for d in domains) + ")"


def _term_filter(terms: list[str]) -> str:
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"


# 欧州各国・その他地域の販売代理店ニュースルームで検索する車名(ロード/レーシング共通、OR結合)。
_DISTRIBUTOR_NAME_FILTER = _term_filter(["GR Supra"] + _RACING_NAMES_EN)

# 欧州以外の地域の公式販売代理店ニュースルーム(2026-09-06追加、第2弾)。
# 南アフリカ(TSAM)は専用メディアサブドメインが見つからず、toyota.co.za本体がそれを兼ねる。
# EU各国と同様、国ごとのロケールを合わせないと0件になる(南アフリカはen-US等では検索結果
# 0件、en-ZA/ZA/ZA:enに合わせて初めて公式記事がヒットすることを確認済み)。
_OTHER_DISTRIBUTOR_SITES: dict[str, tuple[str, str, str, str]] = {
    # country_code: (domain, hl, gl, ceid)
    "ZA": ("toyota.co.za", "en-ZA", "ZA", "ZA:en"),
}


QUERIES = [
    # 北米/欧州/豪州/NZ/グローバル公式ニュースルーム — production(グレード別)
    *[(f'"{trim}" {_site_filter(_OFFICIAL_SITES_EN)}', "en-US", "US", "US:en") for trim in _GLOBAL_TRIMS],
    # 日本(トヨタ自動車公式サイト。GR Garage販売店網の公式ハブページもtoyota.jp配下)
    ("GRスープラ site:toyota.jp", "ja", "JP", "JP:ja"),
    *[(f"{trim} site:toyota.jp", "ja", "JP", "JP:ja") for trim in _JP_TRIMS],
    # レーシング(GT4 / GT500) — TOYOTA GAZOO Racing公式 + 英語圏公式ニュースルーム
    *[(f'"{name}" {_site_filter(_RACING_SITES_EN)}', "en-US", "US", "US:en") for name in _RACING_NAMES_EN],
    *[(f"{name} site:toyotagazooracing.com", "ja", "JP", "JP:ja") for name in _RACING_NAMES_JP],
    # 欧州各国の公式販売代理店(英・独・伊・西) — newsroom.toyota.euとは別ドメイン
    *[
        (f"{_DISTRIBUTOR_NAME_FILTER} site:{domain}", hl, gl, ceid)
        for domain, hl, gl, ceid in _EU_DISTRIBUTOR_SITES.values()
    ],
    # 南アフリカ(TSAM) — toyota.co.za本体(専用メディアサブドメインなし)
    *[
        (f"{_DISTRIBUTOR_NAME_FILTER} site:{domain}", hl, gl, ceid)
        for domain, hl, gl, ceid in _OTHER_DISTRIBUTOR_SITES.values()
    ],
    # 日本の販売会社(GR Garage網中心の代表サンプル) — production(グレード別)
    (f"GRスープラ {_site_filter(_JP_DEALER_SITES)}", "ja", "JP", "JP:ja"),
    *[(f"{trim} {_site_filter(_JP_DEALER_SITES)}", "ja", "JP", "JP:ja") for trim in _JP_TRIMS],
]


def fetch(limit_per_query: int = 8) -> list[dict]:
    items: list[dict] = []
    for query, hl, gl, ceid in QUERIES:
        items.extend(fetch_google_news_rss(query, hl=hl, gl=gl, ceid=ceid, limit=limit_per_query))
    return sort_by_recency(dedupe_by_url(items))
