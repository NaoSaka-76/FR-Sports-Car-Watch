(function () {
  "use strict";

  var LANG_STORAGE_KEY = "frSportsCarWatchLang";

  var ICONS = {
    flag:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3v18"/><path d="M5 4h14l-3 3.5 3 3.5H5z"/></svg>',
    gear:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 13a1.7 1.7 0 000-2l1.4-1.2-2-3.4-1.8.6a1.7 1.7 0 00-1.7-1L15 4h-6l-.3 1.9a1.7 1.7 0 00-1.7 1l-1.8-.6-2 3.4L4.6 11a1.7 1.7 0 000 2l-1.4 1.2 2 3.4 1.8-.6a1.7 1.7 0 001.7 1L9 20h6l.3-1.9a1.7 1.7 0 001.7-1l1.8.6 2-3.4z"/></svg>',
    play:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/></svg>',
    alert:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l9.5 16H2.5z"/><line x1="12" y1="10" x2="12" y2="14.5"/><circle cx="12" cy="17.3" r="0.9" fill="currentColor" stroke="none"/></svg>',
    car:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16.5V12l1.8-5A2 2 0 017.7 5.5h8.6a2 2 0 011.9 1.5l1.8 5v4.5"/><path d="M4 16.5h16"/><path d="M4 16.5v2.3a1 1 0 001 1h1.2a1 1 0 001-1v-2.3"/><path d="M16.8 16.5v2.3a1 1 0 001 1H19a1 1 0 001-1v-2.3"/><circle cx="7.5" cy="13.2" r="1.1" fill="currentColor" stroke="none"/><circle cx="16.5" cy="13.2" r="1.1" fill="currentColor" stroke="none"/></svg>',
    newspaper:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h13v14H4z"/><path d="M17 8h3v11a2 2 0 01-2 2H8"/><path d="M7 9h7M7 12h7M7 15h4"/></svg>',
    trend:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></svg>',
    clock:
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2"/><path d="M9 2h6"/></svg>',
  };

  // 表示順: ①公式リリース → ②ライバル車カタログ → ③ライバル車トピックス → ④ライバル車YouTube
  // → ⑤歴代Supra YouTube → ⑥直6エンジントピックス → ⑦顧客の声/クレーム → ⑧モータースポーツ
  var LAYOUT = [
    { key: "official_news", icon: "newspaper" },
    { key: "rival_topics", icon: "trend" },
    { key: "rival_youtube", icon: "play" },
    { key: "historic_youtube", icon: "clock" },
    { key: "inline_six", icon: "gear" },
    { key: "complaints", icon: "alert" },
    { key: "motorsports", icon: "flag" },
  ];

  // ---- i18n --------------------------------------------------------------
  var I18N = {
    ja: {
      loading: "データを取得しています…",
      updateInterval: "30分毎",
      chipLabel: "自動更新",
      lastUpdatedPrefix: "最終更新: ",
      lastUpdatedUnknown: "不明",
      fetchErrorPrefix: "ダッシュボードデータの読み込みに失敗しました(",
      fetchErrorSuffix: ")。",
      statusFetchFailed: "更新情報を取得できませんでした",
      footer:
        "本ダッシュボードは公開情報源(Googleニュース検索・YouTube検索結果・各シリーズ公式サイト・" +
        "Wikimedia Commons)を自動集計した非公式のモニタリングツールです。トヨタ自動車の公式発表とは" +
        "異なる場合があります。Googleニュースの記事本文は取得できないため見出しのみを対象とし、" +
        "ポジティブ/ネガティブ表示は見出し文のみに基づく自動推定(簡易辞書・VADER)で参考値です。" +
        "JavaScriptで描画される公式サイト(Formula Drift US・Supercars等)は誤表示を避けるため一覧化せず" +
        "公式サイトへのリンクのみを提供しています。真のリアルタイム更新ではなく、30分毎のバッチ更新です。",
      statTotal: "本日の総情報件数",
      statYoutube: "YouTube動画件数",
      statMotorsports: "モータースポーツ関連話題({n}シリーズ)",
      unitItems: "件",
      unitVideos: "本",
      unitSeries: "シリーズ",
      emptyGeneric: "現在、該当する情報はありません。",
      emptyGroup: "該当情報なし",
      emptySchedule: "日程情報を取得できませんでした。",
      tabNewest: "新着順",
      tabPopular: "話題順",
      tabPopularViews: "再生数順",
      groupTopics: "トピックス",
      groupResults: "最新レース結果",
      groupStandings: "ランキング関連ニュース",
      groupSchedule: "レース日程",
      groupRanking: "シリーズランキング",
      nextRace: "次戦",
      linkCalendar: "公式カレンダーを見る ↗",
      linkStandings: "公式ランキングを見る ↗",
      linkOfficial: "公式サイトを見る ↗",
      scheduleLinkNote: "日程データの構造が不安定なため一覧化を見送っています。公式カレンダーは以下のリンクからご確認ください。",
      standingsNoteError: "ランキングの取得中にエラーが発生しました。「公式ランキングを見る」からご確認ください。",
      sentimentPositive: "ポジティブ",
      sentimentNegative: "ネガティブ",
      sentimentReasonsPrefix: "判定根拠: ",
      sentimentSuffixPositive: " という語がポジティブと判定されました",
      sentimentSuffixNegative: " という語がネガティブと判定されました",
      titleUnknown: "(タイトル不明)",
      photoCredit: "写真: ",
      viaCommons: "、Wikimedia Commonsより",
      productionStatusLabel: "生産状況: ",
      trimTopBadge: "最上位/特別仕様",
      trimBaseBadge: "最廉価",
      sections: {
        official_news: {
          title: "① 公式リリース(GRスープラ / GT4 / GT500)",
          note:
            "トヨタ自動車および各地域(日本・北米・欧州・オセアニア)の販売会社によるGRスープラ" +
            "(市販車 A90/A91)、Supra GT4、Supra GT500(SUPER GT)の公式プレスリリースを新着順で集約。",
        },
        rivals_catalog: {
          title: "② ライバル車カタログ",
        },
        rival_topics: {
          title: "③ ライバル車トピックス",
          note:
            "GRスープラのライバル車に関するニュースをGoogleニュースRSSから車種別に集約しています。" +
            "「話題順」は検索結果内での表示順(関連度順)を代替指標として用いたものであり、" +
            "実際のエンゲージメント数ではありません(記事本文が取得できないため)。",
        },
        rival_youtube: {
          title: "④ ライバル車YouTube",
          note:
            "GRスープラのライバル車に関するYouTube動画を車種別に集約しています。" +
            "「再生数順」は検索結果ページに表示された再生回数に基づく実データです。",
        },
        historic_youtube: {
          title: "⑤ 歴代Supra YouTube(全世代)",
          note:
            "A40/A50(セリカスープラ)からA90/A91(現行GRスープラ)まで、Supraの全世代についての" +
            "YouTube動画を世代別に集約しています。世代タブで絞り込み、新着順/再生数順を切り替えられます。" +
            "旧世代(A40/A50・A60)は情報量が少なく該当動画が薄い場合があります。",
        },
        inline_six: {
          title: "⑥ 世界の直列6気筒エンジントピックス",
          note:
            "Supra専用のセクションではなく、BMW B58・Mercedes-AMG M256・マツダ直6(e-Skyactiv)・" +
            "日産VR30DDTT・Jaguar Ingenium I6・Genesis/Hyundai Smartstream I6等、直列6気筒(インライン6)" +
            "エンジン技術に関する世界のニュースを全メーカー横断で集約しています。Supra自身の2JZ/B58由来" +
            "エンジンもこの中の一トピックとして含まれますが、主眼ではありません。「話題順」は検索結果の" +
            "表示順(関連度順)によるものです。",
        },
        complaints: {
          title: "⑦ Supra 顧客の声・クレーム",
          note:
            "社内クレーム管理システムとは未連携です。市販GRスープラに関するニュース報道(リコール等)で" +
            "公開されている情報のみを集約した簡易モニタリングです。「話題順」は検索結果内での表示順" +
            "(関連度順)を代替指標として用いています(実際のSNS拡散数やエンゲージメント数ではありません)。",
        },
        motorsports: {
          title: "⑧ Supra モータースポーツ",
          note:
            "GT500・GT300・フォーミュラドリフト(日本・米国)・D1GP・Supercars Championship等、" +
            "GRスープラ/Supraが参戦するシリーズを地域別に集約。日程・ランキングはSUPER GT公式サイト等" +
            "静的HTMLの実データ、JavaScript描画のサイト(Formula Drift US・Supercars)は公式サイトへの" +
            "リンクのみです(各カード内に理由を記載)。",
        },
      },
      regions: { japan: "日本", us: "米国", australia: "オーストラリア" },
      series: {
        super_gt_gt500: {
          label: "SUPER GT GT500クラス",
          desc: "TOM'S・セルモ・SARD・ROOKIE・WedsSport Bandoh等、GRスープラを駆るワークスチームが参戦する日本最高峰のGTレース。",
        },
        super_gt_gt300: {
          label: "SUPER GT GT300クラス",
          desc: "Saitama Green Brave Toyota GR Supra等、GRスープラで参戦するチームが存在するプライベーター主体のクラス。",
        },
        formula_drift_japan: {
          label: "Formula Drift Japan(FDJ)",
          desc: "松山英樹(CUSCO Racing)がGRスープラで参戦する日本のドリフト選手権。",
        },
        d1gp: {
          label: "D1GP",
          desc: "齋藤大貴(FAT FIVE RACING)・手塚祥(WEINS Toyota神奈川)がGRスープラで参戦する日本のドリフトグランプリ。",
        },
        formula_drift_pro: {
          label: "Formula Drift(PROクラス)",
          desc: "Fredric Aasbo(Papadakis Racing)・Simen OlsenがGRスープラで参戦する米国のドリフト選手権最高峰クラス。",
        },
        supercars_championship: {
          label: "Supercars Championship(Gen3)",
          desc: "Walkinshaw Andretti Unitedより2026年からGen3規定のGRスープラが新規参入したオーストラリアのツーリングカー選手権。",
        },
      },
      carSpecs: {
        engine: "エンジン",
        power: "最高出力",
        torque: "最大トルク",
        zero_to_60: "0-100km/h加速",
        weight: "車両重量",
        transmission: "トランスミッション",
      },
      generations: {
        a40_a50: "A40/A50(セリカスープラ)",
        a60: "A60(セリカスープラ)",
        a70: "A70(MA70・3代目)",
        a80: "A80(JZA80・4代目・2JZ)",
        a90_a91: "A90/A91(現行GRスープラ)",
      },
      tabAll: "すべて",
      showTrims: "グレード詳細を表示",
      hideTrims: "グレード詳細を隠す",
    },
    en: {
      loading: "Loading data…",
      updateInterval: "Every 30 min",
      chipLabel: "auto-update",
      lastUpdatedPrefix: "Last updated: ",
      lastUpdatedUnknown: "unknown",
      fetchErrorPrefix: "Failed to load dashboard data (",
      fetchErrorSuffix: ").",
      statusFetchFailed: "Could not fetch update status",
      footer:
        "This dashboard is an unofficial monitoring tool that automatically aggregates public sources " +
        "(Google News search, YouTube search results, each series' official site, and Wikimedia Commons). " +
        "It may differ from Toyota Motor Corporation's official announcements. Google News article body text " +
        "isn't retrievable, so only headlines are used, and positive/negative labels are automatic estimates " +
        "based on headline text only (a simple lexicon and VADER) — reference values only. JS-rendered official " +
        "sites (Formula Drift US, Supercars, etc.) are intentionally link-out only rather than scraped, to avoid " +
        "misrepresenting data. This is a 30-minute batch update, not true real-time.",
      statTotal: "Total items today",
      statYoutube: "YouTube videos",
      statMotorsports: "Motorsports topics ({n} series)",
      unitItems: "items",
      unitVideos: "videos",
      unitSeries: "series",
      emptyGeneric: "No matching information right now.",
      emptyGroup: "Nothing to show",
      emptySchedule: "Could not fetch schedule information.",
      tabNewest: "Newest",
      tabPopular: "Trending",
      tabPopularViews: "Most viewed",
      groupTopics: "Topics",
      groupResults: "Latest Results",
      groupStandings: "Ranking News",
      groupSchedule: "Race Schedule",
      groupRanking: "Series Ranking",
      nextRace: "Next round",
      linkCalendar: "View official calendar ↗",
      linkStandings: "View official ranking ↗",
      linkOfficial: "Visit official site ↗",
      scheduleLinkNote: "The schedule data structure is unstable, so it isn't listed here. Please check the official calendar via the link below.",
      standingsNoteError: "An error occurred while fetching the ranking. Please check via \"View official ranking.\"",
      sentimentPositive: "Positive",
      sentimentNegative: "Negative",
      sentimentReasonsPrefix: "Detected words: ",
      sentimentSuffixPositive: " — classified as positive",
      sentimentSuffixNegative: " — classified as negative",
      titleUnknown: "(untitled)",
      trimTopBadge: "Top / special edition",
      trimBaseBadge: "Base / cheapest",
      photoCredit: "Photo: ",
      viaCommons: ", via Wikimedia Commons",
      productionStatusLabel: "Production status: ",
      sections: {
        official_news: {
          title: "① Official Releases (GR Supra / GT4 / GT500)",
          note:
            "Official press releases from Toyota Motor Corporation and regional dealers/importers " +
            "(Japan, North America, Europe, Oceania) covering the road-going GR Supra (A90/A91), Supra GT4, " +
            "and Supra GT500 (SUPER GT), sorted newest first.",
        },
        rivals_catalog: { title: "② Rival Vehicle Catalog" },
        rival_topics: {
          title: "③ Rival Vehicle Topics",
          note:
            "News about the GR Supra's rival vehicles, aggregated from Google News RSS per vehicle. " +
            "\"Trending\" uses search-result display order (relevance ranking) as a proxy — not actual " +
            "engagement, since article body text isn't retrievable.",
        },
        rival_youtube: {
          title: "④ Rival Vehicle YouTube",
          note:
            "YouTube videos about the GR Supra's rival vehicles, aggregated per vehicle. " +
            "\"Most viewed\" is real data based on the view count shown on the search results page.",
        },
        historic_youtube: {
          title: "⑤ Historic Supra YouTube (All Generations)",
          note:
            "YouTube videos covering every Supra generation, from the A40/A50 (Celica Supra) through the " +
            "current A90/A91 GR Supra, grouped by generation. Use the generation tabs to filter, and toggle " +
            "newest/most-viewed. Older generations (A40/A50, A60) may return thinner results.",
        },
        inline_six: {
          title: "⑥ Worldwide Inline-Six Engine Topics",
          note:
            "Not Supra-specific — aggregates news about inline-six (straight-six) engine technology across " +
            "all manufacturers: BMW B58, Mercedes-AMG M256, Mazda's inline-six (e-Skyactiv), Nissan VR30DDTT, " +
            "Jaguar Ingenium I6, Genesis/Hyundai Smartstream I6, and more. The Supra's own 2JZ/B58-derived " +
            "engine is one thread among these, not the focus. \"Trending\" reflects search-result display order.",
        },
        complaints: {
          title: "⑦ Supra Customer Voice & Complaints",
          note:
            "Not connected to any internal complaint-management system. Aggregates only publicly reported " +
            "news (e.g. recalls) about the production GR Supra. \"Trending\" uses search-result display order " +
            "as a proxy for attention (not actual share/engagement counts).",
        },
        motorsports: {
          title: "⑧ Supra Motorsports",
          note:
            "GT500, GT300, Formula Drift (Japan & US), D1GP, and the Supercars Championship — every series " +
            "the GR Supra / Supra races in, grouped by region. Schedules/standings use real data from static-HTML " +
            "official sites (e.g. SUPER GT); JS-rendered sites (Formula Drift US, Supercars) are link-out only " +
            "(reason noted on each card).",
        },
      },
      regions: { japan: "Japan", us: "United States", australia: "Australia" },
      series: {
        super_gt_gt500: {
          label: "SUPER GT GT500 Class",
          desc: "Japan's top-tier GT series, where works teams (TOM'S, Cerumo, SARD, ROOKIE, WedsSport Bandoh, etc.) run the GR Supra.",
        },
        super_gt_gt300: {
          label: "SUPER GT GT300 Class",
          desc: "A privateer-heavy class that includes GR Supra entries such as the Saitama Green Brave Toyota GR Supra.",
        },
        formula_drift_japan: {
          label: "Formula Drift Japan (FDJ)",
          desc: "Japan's drift championship, where Hokuto Matsuyama (CUSCO Racing) competes in a GR Supra.",
        },
        d1gp: {
          label: "D1GP",
          desc: "Japan's drift grand prix, where Daigo Saito (FAT FIVE RACING) and Tsuyoshi Tezuka (WEINS Toyota Kanagawa) run GR Supras.",
        },
        formula_drift_pro: {
          label: "Formula Drift (Pro Class)",
          desc: "The top class of the US drift championship, where Fredric Aasbo (Papadakis Racing) and Simen Olsen run GR Supras.",
        },
        supercars_championship: {
          label: "Supercars Championship (Gen3)",
          desc: "Australia's touring car championship, which the Gen3-spec GR Supra joins new in 2026 via Walkinshaw Andretti United.",
        },
      },
      carSpecs: {
        engine: "Engine",
        power: "Max Power",
        torque: "Max Torque",
        zero_to_60: "0-60mph",
        weight: "Weight",
        transmission: "Transmission",
      },
      generations: {
        a40_a50: "A40/A50 (Celica Supra)",
        a60: "A60 (Celica Supra)",
        a70: "A70 (MA70, Mk3)",
        a80: "A80 (JZA80, Mk4, 2JZ)",
        a90_a91: "A90/A91 (Current GR Supra)",
      },
      tabAll: "All",
      showTrims: "Show grade details",
      hideTrims: "Hide grade details",
    },
  };

  var LANG = (function () {
    try {
      var saved = window.localStorage.getItem(LANG_STORAGE_KEY);
      if (saved === "ja" || saved === "en") return saved;
    } catch (e) {
      /* localStorage unavailable */
    }
    return "ja";
  })();

  function t() {
    return I18N[LANG] || I18N.ja;
  }

  function pick(value) {
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return value[LANG] || value.ja || value.en || "";
    }
    return value || "";
  }

  var board = document.getElementById("board");
  var statsEl = document.getElementById("stats");
  var lastUpdatedEl = document.getElementById("last-updated");
  var statusDot = document.getElementById("status-dot");
  var chipLabelEl = document.getElementById("chip-label");
  var updateIntervalChipEl = document.getElementById("update-interval-chip");
  var loadingEl = document.getElementById("loading");
  var footerTextEl = document.getElementById("footer-text");
  var langToggleEl = document.getElementById("lang-toggle");

  var lastData = null;
  var lastCarsData = null;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function formatPublished(raw) {
    if (!raw) return "";
    var parsed = new Date(raw);
    if (!isNaN(parsed.getTime()) && /\d{4}/.test(raw)) {
      return parsed.toLocaleString(LANG === "en" ? "en-US" : "ja-JP", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    }
    return raw;
  }

  function sentimentPill(sentiment) {
    if (!sentiment || sentiment.label === "neutral") return null;
    var s = t();
    var isPositive = sentiment.label === "positive";
    var pill = el(
      "span",
      "sentiment-pill sentiment-pill--" + sentiment.label,
      (isPositive ? "▲ " : "▼ ") + (isPositive ? s.sentimentPositive : s.sentimentNegative)
    );
    var reasons = sentiment.reasons || [];
    if (reasons.length > 0) {
      var tip = s.sentimentReasonsPrefix + reasons.join(" / ") + (isPositive ? s.sentimentSuffixPositive : s.sentimentSuffixNegative);
      pill.setAttribute("data-tip", tip);
      pill.tabIndex = 0;
    }
    return pill;
  }

  function buildItem(item) {
    var s = t();
    var sentimentLabel = item.sentiment ? item.sentiment.label : "neutral";
    var a = el("a", "item item--" + sentimentLabel);
    a.href = item.url || "#";
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    if (!item.url) {
      a.removeAttribute("href");
      a.style.cursor = "default";
    }

    if (item.thumbnail) {
      var img = el("img", "item__thumb");
      img.src = item.thumbnail;
      img.alt = "";
      img.loading = "lazy";
      a.appendChild(img);
    }

    var body = el("div", "item__body");
    body.appendChild(el("span", "item__title", item.title || s.titleUnknown));

    var meta = el("div", "item__meta");
    var pill = sentimentPill(item.sentiment);
    if (pill) meta.appendChild(pill);
    if (item.source) meta.appendChild(el("span", null, item.source));
    var published = formatPublished(item.published);
    if (published) meta.appendChild(el("span", null, published));
    if (item.view_count_text) {
      meta.appendChild(el("span", "item__metric", item.view_count_text));
    }
    body.appendChild(meta);
    a.appendChild(body);

    return a;
  }

  function buildList(items) {
    var list = el("ul", "panel__list");
    items.forEach(function (item) {
      var li = el("li");
      li.appendChild(buildItem(item));
      list.appendChild(li);
    });
    return list;
  }

  function buildPanelHeader(icon, label, count) {
    var header = el("div", "panel__header");
    var iconWrap = el("div", "panel__icon");
    iconWrap.innerHTML = ICONS[icon] || "";
    header.appendChild(iconWrap);
    header.appendChild(el("h2", "panel__title", label));
    if (count !== undefined) header.appendChild(el("span", "panel__count", count + " " + t().unitItems));
    return header;
  }

  // ---- ① 公式リリース(単純リスト) ----------------------------------------

  function buildOfficialNewsPanel(icon, section) {
    var s = t();
    var meta = s.sections.official_news;
    var panel = el("section", "panel panel--full");
    var items = section.items || [];
    panel.appendChild(buildPanelHeader(icon, meta.title, items.length));
    if (meta.note) panel.appendChild(el("p", "panel__note", meta.note));
    if (items.length === 0) {
      panel.appendChild(el("p", "panel__empty", s.emptyGeneric));
    } else {
      panel.appendChild(buildList(items));
    }
    return panel;
  }

  // ---- 汎用: 新着/話題(または再生数)の2タブパネル -------------------------

  function buildTwoTabPanel(icon, sectionKey, listA, listB, labelBOverride, count) {
    var s = t();
    var meta = s.sections[sectionKey] || {};
    var panel = el("section", "panel panel--full");
    panel.appendChild(buildPanelHeader(icon, meta.title || sectionKey, count !== undefined ? count : listA.length));
    if (meta.note) panel.appendChild(el("p", "panel__note", meta.note));

    var tabs = el("div", "tab-group");
    var tabA = el("button", "tab-group__btn is-active", s.tabNewest);
    var tabB = el("button", "tab-group__btn", labelBOverride || s.tabPopular);
    tabs.appendChild(tabA);
    tabs.appendChild(tabB);
    panel.appendChild(tabs);

    var listWrap = el("div");
    function renderList(items) {
      listWrap.innerHTML = "";
      if (!items || items.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", s.emptyGeneric));
      } else {
        listWrap.appendChild(buildList(items));
      }
    }
    renderList(listA);
    panel.appendChild(listWrap);

    tabA.addEventListener("click", function () {
      tabA.classList.add("is-active");
      tabB.classList.remove("is-active");
      renderList(listA);
    });
    tabB.addEventListener("click", function () {
      tabB.classList.add("is-active");
      tabA.classList.remove("is-active");
      renderList(listB);
    });

    return panel;
  }

  // ---- ③④ ライバル車トピックス/YouTube(統合リスト + 車種選択タブ) --------

  function mergeAllRivals(rivals, sortKey) {
    var seen = {};
    var merged = [];
    function pushUnique(item) {
      var k = item.url || item.video_id;
      if (k && seen[k]) return;
      if (k) seen[k] = true;
      merged.push(item);
    }
    var pools = (rivals || []).map(function (r) { return r[sortKey] || []; });

    if (sortKey === "newest") {
      // recency_seconds(YouTube)またはRSSのpublished日時(ニュース)で、
      // 車種をまたいだ真の時系列順にソートする。
      var flat = [].concat.apply([], pools);
      flat.sort(function (a, b) {
        if (a.recency_seconds !== undefined && b.recency_seconds !== undefined) {
          return a.recency_seconds - b.recency_seconds;
        }
        var ta = a.published ? Date.parse(a.published) : 0;
        var tb = b.published ? Date.parse(b.published) : 0;
        return tb - ta;
      });
      flat.forEach(pushUnique);
    } else {
      var hasViewCount = pools.some(function (p) { return p.length > 0 && p[0].view_count !== undefined; });
      if (hasViewCount) {
        // YouTube再生数は車種をまたいで比較可能な実数なので、そのままグローバルソート。
        var flat2 = [].concat.apply([], pools);
        flat2.sort(function (a, b) { return (b.view_count || 0) - (a.view_count || 0); });
        flat2.forEach(pushUnique);
      } else {
        // ニュースの「話題順」は検索結果内の関連度順(車種ごとの相対順位のみ)で、
        // 車種をまたいで比較可能なスコアがないため、各車種の順位を保ったまま
        // ラウンドロビンで均等に混ぜる(特定の車種の結果だけが上位を占めないように)。
        var maxLen = pools.reduce(function (m, p) { return Math.max(m, p.length); }, 0);
        for (var i = 0; i < maxLen; i++) {
          pools.forEach(function (p) { if (i < p.length) pushUnique(p[i]); });
        }
      }
    }
    return merged;
  }

  function buildRivalUnifiedPanel(icon, sectionKey, rivals, labelB) {
    var s = t();
    var meta = s.sections[sectionKey] || {};
    var panel = el("section", "panel panel--full");
    var totalCount = (rivals || []).reduce(function (sum, r) {
      return sum + (r.newest ? r.newest.length : 0);
    }, 0);
    panel.appendChild(buildPanelHeader(icon, meta.title || sectionKey, totalCount));
    if (meta.note) panel.appendChild(el("p", "panel__note", meta.note));

    var vehicleTabs = el("div", "tab-group");
    var sortTabs = el("div", "tab-group");
    panel.appendChild(vehicleTabs);
    panel.appendChild(sortTabs);

    var listWrap = el("div");
    panel.appendChild(listWrap);

    var ALL_RIVALS = -1;
    var activeIndex = ALL_RIVALS; // 既定: すべて(全車種を統合表示)
    var activeSort = "newest";

    var allBtn = el("button", "tab-group__btn tab-group__btn--gen is-active", s.tabAll);
    allBtn.addEventListener("click", function () {
      activeIndex = ALL_RIVALS;
      allBtn.classList.add("is-active");
      vehicleButtons.forEach(function (b) { b.classList.remove("is-active"); });
      renderCurrent();
    });
    vehicleTabs.appendChild(allBtn);

    var vehicleButtons = (rivals || []).map(function (rival, idx) {
      var btn = el("button", "tab-group__btn tab-group__btn--gen", rival.label);
      btn.addEventListener("click", function () {
        activeIndex = idx;
        allBtn.classList.remove("is-active");
        vehicleButtons.forEach(function (b, i) { b.classList.toggle("is-active", i === idx); });
        renderCurrent();
      });
      vehicleTabs.appendChild(btn);
      return btn;
    });

    var sortNewestBtn = el("button", "tab-group__btn is-active", s.tabNewest);
    var sortBBtn = el("button", "tab-group__btn", labelB);
    sortNewestBtn.addEventListener("click", function () {
      activeSort = "newest";
      sortNewestBtn.classList.add("is-active");
      sortBBtn.classList.remove("is-active");
      renderCurrent();
    });
    sortBBtn.addEventListener("click", function () {
      activeSort = "popular";
      sortBBtn.classList.add("is-active");
      sortNewestBtn.classList.remove("is-active");
      renderCurrent();
    });
    sortTabs.appendChild(sortNewestBtn);
    sortTabs.appendChild(sortBBtn);

    function renderCurrent() {
      listWrap.innerHTML = "";
      var items;
      if (activeIndex === ALL_RIVALS) {
        items = mergeAllRivals(rivals, activeSort);
      } else {
        var rival = (rivals || [])[activeIndex];
        items = rival ? rival[activeSort] : [];
      }
      if (!items || items.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", s.emptyGeneric));
      } else {
        listWrap.appendChild(buildList(items));
      }
    }
    renderCurrent();

    return panel;
  }

  // ---- ⑤ 歴代Supra YouTube(世代タブ + 新着/再生数タブ) --------------------

  function buildHistoricYoutubePanel(icon, section) {
    var s = t();
    var meta = s.sections.historic_youtube;
    var generations = section.generations || [];
    var panel = el("section", "panel panel--full");
    var totalCount = generations.reduce(function (sum, g) { return sum + (g.newest ? g.newest.length : 0); }, 0);
    panel.appendChild(buildPanelHeader(icon, meta.title, totalCount));
    if (meta.note) panel.appendChild(el("p", "panel__note", meta.note));

    var genTabs = el("div", "tab-group");
    var sortTabs = el("div", "tab-group");
    panel.appendChild(genTabs);
    panel.appendChild(sortTabs);

    var listWrap = el("div");
    panel.appendChild(listWrap);

    var ALL_GENERATIONS = -1;
    var activeGenIndex = ALL_GENERATIONS; // 既定: すべて(全世代を統合表示)
    var activeSort = "newest";

    var allBtn = el(
      "button",
      "tab-group__btn tab-group__btn--gen" + (activeGenIndex === ALL_GENERATIONS ? " is-active" : ""),
      s.tabAll
    );
    allBtn.addEventListener("click", function () {
      activeGenIndex = ALL_GENERATIONS;
      allBtn.classList.add("is-active");
      genButtons.forEach(function (b) { b.classList.remove("is-active"); });
      renderCurrent();
    });
    genTabs.appendChild(allBtn);

    var genButtons = generations.map(function (gen, idx) {
      var label = s.generations[gen.key] || gen.label;
      var btn = el("button", "tab-group__btn tab-group__btn--gen" + (idx === activeGenIndex ? " is-active" : ""), label);
      btn.addEventListener("click", function () {
        activeGenIndex = idx;
        allBtn.classList.remove("is-active");
        genButtons.forEach(function (b, i) { b.classList.toggle("is-active", i === idx); });
        renderCurrent();
      });
      genTabs.appendChild(btn);
      return btn;
    });

    function mergeAllGenerations(sortKey) {
      var seen = {};
      var merged = [];
      generations.forEach(function (gen) {
        (gen[sortKey] || []).forEach(function (item) {
          var dedupeKey = item.url || item.video_id;
          if (dedupeKey && seen[dedupeKey]) return;
          if (dedupeKey) seen[dedupeKey] = true;
          merged.push(item);
        });
      });
      if (sortKey === "popular") {
        merged.sort(function (a, b) { return (b.view_count || 0) - (a.view_count || 0); });
      } else {
        merged.sort(function (a, b) { return (a.recency_seconds || 0) - (b.recency_seconds || 0); });
      }
      return merged;
    }

    var sortNewestBtn = el("button", "tab-group__btn is-active", s.tabNewest);
    var sortPopularBtn = el("button", "tab-group__btn", s.tabPopularViews);
    sortNewestBtn.addEventListener("click", function () {
      activeSort = "newest";
      sortNewestBtn.classList.add("is-active");
      sortPopularBtn.classList.remove("is-active");
      renderCurrent();
    });
    sortPopularBtn.addEventListener("click", function () {
      activeSort = "popular";
      sortPopularBtn.classList.add("is-active");
      sortNewestBtn.classList.remove("is-active");
      renderCurrent();
    });
    sortTabs.appendChild(sortNewestBtn);
    sortTabs.appendChild(sortPopularBtn);

    function renderCurrent() {
      listWrap.innerHTML = "";
      var items;
      if (activeGenIndex === ALL_GENERATIONS) {
        items = mergeAllGenerations(activeSort);
      } else {
        var gen = generations[activeGenIndex];
        items = gen ? gen[activeSort] : [];
      }
      if (!items || items.length === 0) {
        listWrap.appendChild(el("p", "panel__empty", s.emptyGeneric));
      } else {
        listWrap.appendChild(buildList(items));
      }
    }
    renderCurrent();

    return panel;
  }

  // ---- ⑧ モータースポーツ(地域別シリーズカード) ---------------------------

  function buildSeriesGroup(title, items) {
    var group = el("div", "series-card__group");
    group.appendChild(el("div", "series-card__group-title", title));
    if (!items || items.length === 0) {
      group.appendChild(el("p", "panel__empty", t().emptyGroup));
    } else {
      group.appendChild(buildList(items));
    }
    return group;
  }

  function buildStandingsChart(rows) {
    var maxPoints = rows.reduce(function (m, r) { return Math.max(m, r.points); }, 1);
    var chart = el("div", "standings-chart");
    rows.forEach(function (row) {
      var rowEl = el("div", "standings-chart__row" + (row.is_supra ? " standings-chart__row--spotlight" : ""));
      rowEl.appendChild(el("span", "standings-chart__pos", String(row.position)));

      var main = el("div", "standings-chart__main");
      var nameLine = el("div", "standings-chart__name-line");
      nameLine.appendChild(el("span", "standings-chart__name", row.name));
      if (row.is_supra) {
        nameLine.appendChild(el("span", "supra-tag", "GR SUPRA"));
      }
      main.appendChild(nameLine);
      if (row.car) main.appendChild(el("span", "standings-chart__sub", row.car));

      var track = el("div", "standings-chart__track");
      var fill = el("div", "standings-chart__fill");
      fill.style.width = Math.max(4, (100 * row.points) / maxPoints) + "%";
      track.appendChild(fill);
      main.appendChild(track);

      rowEl.appendChild(main);
      rowEl.appendChild(el("span", "standings-chart__points", String(row.points)));
      chart.appendChild(rowEl);
    });
    return chart;
  }

  function buildScheduleBlock(s2) {
    var i18n = t();
    var wrap = el("div", "series-card__group");
    wrap.appendChild(el("div", "series-card__group-title", i18n.groupSchedule));

    if (s2.schedule_link && (!s2.schedule || s2.schedule.length === 0)) {
      wrap.appendChild(el("p", "panel__note series-card__chart-note", i18n.scheduleLinkNote));
      var link = el("a", "series-card__link", i18n.linkCalendar);
      link.href = s2.schedule_link;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      wrap.appendChild(link);
      return wrap;
    }

    var rounds = s2.schedule || [];
    if (rounds.length === 0) {
      wrap.appendChild(el("p", "panel__empty", i18n.emptySchedule));
      return wrap;
    }

    var nextRace = rounds.filter(function (round) { return round.status === "upcoming"; })[0];
    if (nextRace) {
      var next = el("div", "schedule-next");
      next.appendChild(el("span", "schedule-next__label", i18n.nextRace));
      next.appendChild(el("span", "schedule-next__date", nextRace.date_range));
      next.appendChild(
        el("span", "schedule-next__track", [nextRace.round, nextRace.name, nextRace.track].filter(Boolean).join(" · "))
      );
      wrap.appendChild(next);
    }

    var list = el("ul", "schedule-list");
    rounds.forEach(function (r2) {
      var li = el("li", "schedule-list__item schedule-list__item--" + r2.status);
      li.appendChild(el("span", "schedule-list__dot"));
      li.appendChild(el("span", "schedule-list__date", r2.date_range));
      li.appendChild(el("span", "schedule-list__label", [r2.round, r2.name, r2.track].filter(Boolean).join(" · ")));
      list.appendChild(li);
    });
    wrap.appendChild(list);

    return wrap;
  }

  function buildRankingBlock(s2) {
    var i18n = t();
    var wrap = el("div", "series-card__group");
    wrap.appendChild(el("div", "series-card__group-title", i18n.groupRanking));
    if (s2.standings_chart && s2.standings_chart.length > 0) {
      wrap.appendChild(buildStandingsChart(s2.standings_chart));
    }
    var note = s2.standings_error ? i18n.standingsNoteError : s2.standings_chart_note;
    if (note) wrap.appendChild(el("p", "panel__note series-card__chart-note", note));
    return wrap;
  }

  function buildSeriesCard(regionKey, s2) {
    var i18n = t();
    var entry = i18n.series[s2.key];
    var label = (entry && entry.label) || s2.label || s2.key;
    var desc = entry && entry.desc;
    var card = el("div", "series-card series-card--" + regionKey);
    var header = el("div", "series-card__header");
    header.appendChild(el("span", null, label));
    card.appendChild(header);
    if (desc) card.appendChild(el("p", "series-card__desc", desc));
    card.appendChild(buildScheduleBlock(s2));
    card.appendChild(buildRankingBlock(s2));
    card.appendChild(buildSeriesGroup(i18n.groupTopics, s2.topics));
    card.appendChild(buildSeriesGroup(i18n.groupResults, s2.results));
    card.appendChild(buildSeriesGroup(i18n.groupStandings, s2.standings));

    var link = el("a", "series-card__link", i18n.linkStandings);
    link.href = s2.standings_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    card.appendChild(link);

    return card;
  }

  function buildMotorsportsPanel(icon, section) {
    var i18n = t();
    var meta = i18n.sections.motorsports;
    var panel = el("section", "panel panel--full");
    var regions = section.regions || {};
    var totalCount = Object.values(regions).reduce(function (sum, r) {
      return (
        sum +
        r.series.reduce(function (s2, series) {
          return s2 + series.topics.length + series.results.length + series.standings.length;
        }, 0)
      );
    }, 0);
    panel.appendChild(buildPanelHeader(icon, meta.title, totalCount));
    if (meta.note) panel.appendChild(el("p", "panel__note", meta.note));

    var container = el("div", "motorsports");
    Object.keys(regions).forEach(function (key) {
      var r = regions[key];
      var block = el("div", "motorsports-region");
      var heading = el("div", "motorsports-region__title");
      if (r.flag) heading.appendChild(el("span", "motorsports-region__flag", r.flag));
      heading.appendChild(el("span", null, i18n.regions[key] || r.label || key));
      heading.appendChild(el("span", "motorsports-region__count", r.series.length + " " + i18n.unitSeries));
      block.appendChild(heading);

      var grid = el("div", "motorsports-region__grid");
      r.series.forEach(function (s2) {
        grid.appendChild(buildSeriesCard(key, s2));
      });
      block.appendChild(grid);

      container.appendChild(block);
    });
    panel.appendChild(container);
    return panel;
  }

  // ---- ② ライバル/Supraカタログ -------------------------------------------

  function buildCarCard(car) {
    var i18n = t();
    var card = el("div", "car-card" + (car.is_supra ? " car-card--spotlight" : ""));
    var model = pick(car.model);

    var figure = el("div", "car-card__photo");
    if (car.photo && car.photo.src) {
      var img = el("img");
      img.src = car.photo.src;
      img.alt = car.manufacturer + " " + model;
      img.loading = "lazy";
      figure.appendChild(img);
    } else {
      figure.classList.add("car-card__photo--placeholder");
      var placeholderIcon = el("div", "car-card__photo-icon");
      placeholderIcon.innerHTML = ICONS.car;
      figure.appendChild(placeholderIcon);
    }
    if (car.is_supra) figure.appendChild(el("span", "supra-tag car-card__badge", "GR SUPRA"));
    card.appendChild(figure);

    var body = el("div", "car-card__body");
    body.appendChild(el("span", "car-card__manufacturer", car.manufacturer));
    body.appendChild(el("h3", "car-card__model", model));
    var description = pick(car.description);
    if (description) body.appendChild(el("p", "car-card__desc", description));

    function buildStatusEl(productionStatus) {
      if (!productionStatus) return null;
      var statusText = pick(productionStatus);
      return el(
        "div",
        "car-card__status" + (/discontin|生産終了|終了/i.test(statusText) ? " car-card__status--discontinued" : ""),
        i18n.productionStatusLabel + statusText
      );
    }

    function buildSpecList(specs) {
      var specList = el("dl", "car-card__specs");
      (specs || []).forEach(function (spec) {
        specList.appendChild(el("dt", null, i18n.carSpecs[spec.key] || spec.key));
        specList.appendChild(el("dd", null, pick(spec.value)));
      });
      return specList;
    }

    // グレード(トリム)詳細は既定で非表示。②パネル先頭の一括トグルボタンで
    // 全車両まとめて表示/非表示を切り替える(CSSの.panel--trims-visibleで制御)。
    var trimsWrap = el("div", "car-card__trims");
    if (car.trims && car.trims.length > 0) {
      // 最上位(特別仕様)〜最廉価まで、トリムごとに区切って積み上げ表示。
      car.trims.forEach(function (trim, idx) {
        var trimBlock = el("div", "car-card__trim");
        var trimHead = el("div", "car-card__trim-head");
        trimHead.appendChild(el("span", "car-card__trim-label", pick(trim.label)));
        if (idx === 0) {
          trimHead.appendChild(el("span", "car-card__trim-badge car-card__trim-badge--top", i18n.trimTopBadge));
        } else if (idx === car.trims.length - 1 && car.trims.length > 1) {
          trimHead.appendChild(el("span", "car-card__trim-badge car-card__trim-badge--base", i18n.trimBaseBadge));
        }
        trimBlock.appendChild(trimHead);
        trimBlock.appendChild(el("div", "car-card__price", pick(trim.price)));
        var trimStatusEl = buildStatusEl(trim.production_status);
        if (trimStatusEl) trimBlock.appendChild(trimStatusEl);
        trimBlock.appendChild(buildSpecList(trim.specs));
        trimsWrap.appendChild(trimBlock);
        if (idx < car.trims.length - 1) trimsWrap.appendChild(el("hr", "car-card__trim-divider"));
      });
    } else {
      // 旧スキーマ(単一トリム)へのフォールバック。
      trimsWrap.appendChild(el("div", "car-card__price", pick(car.price)));
      var legacyStatusEl = buildStatusEl(car.production_status);
      if (legacyStatusEl) trimsWrap.appendChild(legacyStatusEl);
      trimsWrap.appendChild(buildSpecList(car.specs));
    }
    body.appendChild(trimsWrap);

    var link = el("a", "series-card__link", i18n.linkOfficial);
    link.href = car.official_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    body.appendChild(link);

    if (car.photo && car.photo.src) {
      var credit = el("p", "car-card__credit");
      credit.appendChild(document.createTextNode(i18n.photoCredit));
      var creditLink = el("a", null, car.photo.credit + " (" + car.photo.license + ")");
      creditLink.href = car.photo.source_url;
      creditLink.target = "_blank";
      creditLink.rel = "noopener noreferrer";
      credit.appendChild(creditLink);
      credit.appendChild(document.createTextNode(i18n.viaCommons));
      body.appendChild(credit);
    }

    card.appendChild(body);
    return card;
  }

  function buildCarsPanel(carsData) {
    var i18n = t();
    var panel = el("section", "panel panel--full");
    var cars = carsData.cars || [];
    panel.appendChild(buildPanelHeader("car", i18n.sections.rivals_catalog.title, cars.length));
    var note = pick(carsData.note);
    if (note) panel.appendChild(el("p", "panel__note", note));

    // グレード詳細の表示/非表示を全車両まとめて切り替える一括ボタン
    // (車両ごとの個別ボタンは持たず、この1つだけで全カードを制御する)。
    var trimsToggleBtn = el("button", "tab-group__btn", i18n.showTrims);
    var trimsVisible = false;
    trimsToggleBtn.addEventListener("click", function () {
      trimsVisible = !trimsVisible;
      panel.classList.toggle("panel--trims-visible", trimsVisible);
      trimsToggleBtn.textContent = trimsVisible ? i18n.hideTrims : i18n.showTrims;
    });
    var toggleWrap = el("div", "tab-group");
    toggleWrap.appendChild(trimsToggleBtn);
    panel.appendChild(toggleWrap);

    var grid = el("div", "car-grid");
    cars.forEach(function (car) {
      grid.appendChild(buildCarCard(car));
    });
    panel.appendChild(grid);
    return panel;
  }

  // ---- 集計・サマリー --------------------------------------------------

  function collectSentimentItems(data) {
    var all = [];
    var official = data.sections.official_news;
    if (official && official.items) all = all.concat(official.items);

    ["rival_topics", "rival_youtube"].forEach(function (key) {
      var section = data.sections[key];
      if (section && section.rivals) {
        section.rivals.forEach(function (r) { all = all.concat(r.newest || []); });
      }
    });

    var historic = data.sections.historic_youtube;
    if (historic && historic.generations) {
      historic.generations.forEach(function (g) { all = all.concat(g.newest || []); });
    }

    var inlineSix = data.sections.inline_six;
    if (inlineSix) all = all.concat(inlineSix.newest || []);

    var complaints = data.sections.complaints;
    if (complaints) all = all.concat(complaints.items_latest || []);

    var ms = data.sections.motorsports;
    if (ms && ms.regions) {
      Object.values(ms.regions).forEach(function (r) {
        r.series.forEach(function (series) {
          all = all.concat(series.topics, series.results, series.standings);
        });
      });
    }
    return all;
  }

  function buildStats(data) {
    var i18n = t();
    statsEl.innerHTML = "";

    var sentimentItems = collectSentimentItems(data);
    var totalCount = sentimentItems.length;

    var youtubeCount = 0;
    ["rival_youtube"].forEach(function (key) {
      var section = data.sections[key];
      if (section && section.rivals) {
        section.rivals.forEach(function (r) { youtubeCount += (r.newest || []).length; });
      }
    });
    var historic = data.sections.historic_youtube;
    if (historic && historic.generations) {
      historic.generations.forEach(function (g) { youtubeCount += (g.newest || []).length; });
    }

    var motorsportsCount = 0;
    var seriesCount = 0;
    if (data.sections.motorsports && data.sections.motorsports.regions) {
      Object.values(data.sections.motorsports.regions).forEach(function (r) {
        seriesCount += r.series.length;
        r.series.forEach(function (series) {
          motorsportsCount += series.topics.length + series.results.length + series.standings.length;
        });
      });
    }

    var t1 = el("div", "stat-tile");
    t1.appendChild(el("div", "stat-tile__label", i18n.statTotal));
    var v1 = el("div", "stat-tile__value", String(totalCount));
    v1.appendChild(el("small", null, i18n.unitItems));
    t1.appendChild(v1);
    statsEl.appendChild(t1);

    var t3 = el("div", "stat-tile");
    t3.appendChild(el("div", "stat-tile__label", i18n.statYoutube));
    var v3 = el("div", "stat-tile__value", String(youtubeCount));
    v3.appendChild(el("small", null, i18n.unitVideos));
    t3.appendChild(v3);
    statsEl.appendChild(t3);

    var t4 = el("div", "stat-tile");
    t4.appendChild(el("div", "stat-tile__label", i18n.statMotorsports.replace("{n}", String(seriesCount))));
    var v4 = el("div", "stat-tile__value", String(motorsportsCount));
    v4.appendChild(el("small", null, i18n.unitItems));
    t4.appendChild(v4);
    statsEl.appendChild(t4);
  }

  function applyStaticText() {
    var i18n = t();
    document.documentElement.lang = LANG;
    if (chipLabelEl) chipLabelEl.textContent = i18n.chipLabel;
    if (updateIntervalChipEl) updateIntervalChipEl.textContent = i18n.updateInterval;
    if (footerTextEl) footerTextEl.textContent = i18n.footer;
    if (langToggleEl) {
      Array.prototype.forEach.call(langToggleEl.querySelectorAll(".lang-toggle__btn"), function (btn) {
        btn.classList.toggle("is-active", btn.getAttribute("data-lang") === LANG);
      });
    }
  }

  function render(data, carsData) {
    lastData = data;
    lastCarsData = carsData;
    applyStaticText();
    buildStats(data);

    board.innerHTML = "";

    var official = data.sections && data.sections.official_news;
    if (official) board.appendChild(buildOfficialNewsPanel("newspaper", official));

    if (carsData) board.appendChild(buildCarsPanel(carsData));

    LAYOUT.forEach(function (entry) {
      if (entry.key === "official_news") return; // 上で個別描画済み
      var section = data.sections && data.sections[entry.key];
      if (!section) return;
      var panel;
      if (entry.key === "motorsports") {
        panel = buildMotorsportsPanel(entry.icon, section);
      } else if (entry.key === "rival_topics") {
        panel = buildRivalUnifiedPanel(entry.icon, entry.key, section.rivals, t().tabPopular);
      } else if (entry.key === "rival_youtube") {
        panel = buildRivalUnifiedPanel(entry.icon, entry.key, section.rivals, t().tabPopularViews);
      } else if (entry.key === "historic_youtube") {
        panel = buildHistoricYoutubePanel(entry.icon, section);
      } else if (entry.key === "inline_six") {
        panel = buildTwoTabPanel(entry.icon, entry.key, section.newest, section.popular);
      } else if (entry.key === "complaints") {
        panel = buildTwoTabPanel(entry.icon, entry.key, section.items_latest, section.items_buzz);
      }
      if (panel) board.appendChild(panel);
    });

    var i18n = t();
    lastUpdatedEl.textContent = i18n.lastUpdatedPrefix + (data.generated_at_jst || i18n.lastUpdatedUnknown);

    var generatedAt = data.generated_at_utc ? new Date(data.generated_at_utc) : null;
    if (generatedAt) {
      var hoursSince = (Date.now() - generatedAt.getTime()) / 36e5;
      statusDot.classList.toggle("is-stale", hoursSince > 2);
    }
  }

  function renderError(message) {
    applyStaticText();
    statsEl.innerHTML = "";
    board.innerHTML = "";
    board.appendChild(el("p", "board__error", message));
    lastUpdatedEl.textContent = t().statusFetchFailed;
    statusDot.classList.add("is-error");
  }

  function setLang(lang) {
    if (lang !== "ja" && lang !== "en") return;
    if (lang === LANG) return;
    LANG = lang;
    try {
      window.localStorage.setItem(LANG_STORAGE_KEY, lang);
    } catch (e) {
      /* localStorage unavailable */
    }
    if (lastData) {
      render(lastData, lastCarsData);
    } else {
      applyStaticText();
      if (loadingEl) loadingEl.textContent = t().loading;
    }
  }

  if (langToggleEl) {
    langToggleEl.addEventListener("click", function (evt) {
      var btn = evt.target.closest(".lang-toggle__btn");
      if (!btn) return;
      setLang(btn.getAttribute("data-lang"));
    });
  }

  applyStaticText();
  if (loadingEl) loadingEl.textContent = t().loading;

  function fetchJson(path) {
    return fetch(path, { cache: "no-store" }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    });
  }

  fetchJson("data/latest.json")
    .then(function (data) {
      fetchJson("data/rivals.json")
        .then(function (carsData) {
          render(data, carsData);
        })
        .catch(function () {
          render(data, null);
        });
    })
    .catch(function (err) {
      renderError(t().fetchErrorPrefix + err.message + t().fetchErrorSuffix);
    });
})();
