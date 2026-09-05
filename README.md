# FR Sports Car Watch

トヨタ GRスープラ(市販車 A90/A91、および競技車両 Supra GT4 / Supra GT500)とライバルFR
スポーツカーに関する情報を1か所に集約するモニタリングダッシュボード。GitHub Actionsで
30分毎(毎時00分・30分)に自動的にデータを収集し、GitHub Pagesで公開する。

**公開ページ:** Settings > Pages で有効化後、`https://<owner>.github.io/FR-Sports-Car-Watch/`

**日英表示切り替え:** ヘッダー右上の「日本語 / English」タブで、サイトのUI文言(パネル見出し・
ボタン・注記・地域/シリーズ名・世代タブ等)を英語表示に切り替えられる。ニュース記事・動画タイトル
など集約コンテンツ自体は原文言語のまま(UI切り替えによる機械翻訳はしない)。選択言語はブラウザに
保存され、次回訪問時も維持される。既定言語は日本語。

**英語見出しの日本語訳併記:** 日本語を含まない(英語等の)見出しには、Google翻訳の公開エンドポイント
(APIキー不要・非公式)による日本語訳を見出し直下に常時併記する。UI言語切り替えとは独立した表示で、
翻訳結果は記事URL単位で`scripts/.translation_cache.json`にキャッシュし、GitHub Actions実行間は
actions/cacheで永続化する(同じ記事を毎回再翻訳しない)。翻訳に失敗した場合は原文見出しのみ表示。

## 掲載している8セクション

画面上部から以下の順に表示される。

| 順 | セクション | 内容 | 取得方法 |
| --- | --- | --- | --- |
| ① | 公式リリース | トヨタ自動車および日本・北米・欧州・オセアニアの販売会社による、市販GRスープラ(A90/A91)・Supra GT4・Supra GT500(SUPER GT)の公式プレスリリース。新着順 | Google News RSS(グレード/変種名ごとに個別クエリを作成しOR統合) |
| ② | ライバル車カタログ | Porsche 911/718 Cayman・Chevrolet Corvette/Camaro・Nissan GT-R/Z・BMW M2/M3/M4・Ford Mustang Dark Horseの計10車種+GRスープラ自身を写真付きで一覧化。価格・エンジン・出力・トルク・0-100km/h・車重・トランスミッション・生産状況(生産終了車は明記)・公式サイトリンクを掲載。GRスープラのカードのみハイライト表示 | 手動収集の参考価格・スペック(静的データ)+ 写真はWikimedia CommonsのCCライセンス画像(撮影者・ライセンスを明記) |
| ③ | ライバル車トピックス | ②の10車種に関するニュースを車種別に集約。「新着順」「話題順」をタブで切り替え | Google News RSS(「話題順」は検索結果内の表示順=関連度順を代替指標として使用。実際のエンゲージメント数ではない) |
| ④ | ライバル車YouTube | ②の10車種に関するYouTube動画を車種別に集約。「新着順」「再生数順」をタブで切り替え | YouTube検索結果ページのスクレイピング(再生数は実データ) |
| ⑤ | 歴代Supra YouTube(全世代) | A40/A50(セリカスープラ)・A60・A70(MA70)・A80(JZA80・2JZ)・A90/A91(現行GRスープラ)の全世代についてのYouTube動画。世代タブで絞り込み、「新着順」「再生数順」を切り替え | YouTube検索結果ページのスクレイピング(世代ごとに個別クエリを作成) |
| ⑥ | 世界の直列6気筒エンジントピックス | Supra専用ではなく、BMW B58・Mercedes-AMG M256・マツダ直6(e-Skyactiv)・日産VR30DDTT・Jaguar Ingenium I6・Genesis/Hyundai Smartstream I6等、全メーカー横断の直6エンジン技術ニュース。Supra自身の2JZ/B58由来エンジンも一トピックとして含む | Google News RSS |
| ⑦ | Supra 顧客の声・クレーム | 市販GRスープラのリコール・不具合報道。「新着順」「話題順」をタブで切り替え | Google News RSS |
| ⑧ | Supra モータースポーツ | GT500・GT300・Formula Drift Japan・D1GP(日本)、Formula Drift Proクラス(米国)、Supercars Championship Gen3(オーストラリア)を地域別に整理。日程・ランキングを表示 | 日本の4シリーズは公式サイトの実データ(下表参照)、米豪2シリーズはニュース(Google News RSS)+公式サイトへのリンク |

「①公式リリース」以外の全セクションには、見出し文からの簡易センチメント判定(ポジティブ/
ネガティブ)を内部的に付与している(英語: VADER+自動車文脈の辞書補正、日本語: 手作り極性辞書)。
判定根拠はバッジへのマウスオーバー(タッチ操作の場合はタップ)で確認できる。あくまで見出し文の
みに基づく自動推定であり、参考値として利用すること。

## モータースポーツ(⑧)の内訳

| 地域 | シリーズ | GR Supra参戦 | 実データ取得 |
| --- | --- | --- | --- |
| 日本 | SUPER GT GT500クラス | TOM'S・セルモ・SARD・ROOKIE・WedsSport Bandoh等のワークスチーム | 公式サイト(supergt.net)から日程・ランキングを実データ取得 |
| 日本 | SUPER GT GT300クラス | Saitama Green Brave Toyota GR Supra等 | 同上(`?gt_class=gt300`パラメータでGT300に絞り込み。実際に絞り込まれることを確認済み) |
| 日本 | Formula Drift Japan(FDJ) | 松山英樹(CUSCO Racing) | 公式サイト(formulad.jp)から日程・ランキングを実データ取得 |
| 日本 | D1GP | 齋藤(FAT FIVE RACING #87)・手塚(WEINS Toyota神奈川 #90) | 公式サイト(d1gp.co.jp)から日程・ランキングを実データ取得 |
| 米国 | Formula Drift(PROクラス) | Fredric Aasbo(Papadakis Racing)・Simen Olsen | ニュース(Google News RSS)+公式サイトへのリンクのみ(下記「既知の制約」参照) |
| オーストラリア | Supercars Championship(Gen3) | Walkinshaw Andretti United(#1 Chaz Mostert・#2 Ryan Wood、Toyota全体で最低4台のGen3 GR Supraが参戦) | ニュース(Google News RSS)+公式サイトへのリンクのみ(下記「既知の制約」参照) |

## 既知の制約

- **公式API未使用**: YouTube Data API・X API・Facebook Graph API のキーは未設定。すべて
  無料の公開エンドポイント(Google News RSS、YouTube検索ページ)をベストエフォートで
  利用しているため、件数の正確性・網羅性は公式APIに劣る。
- **記事本文は取得できない**: Google News RSSのリンクは `news.google.com` のJS描画
  インタースティシャルを経由するため、`requests` では実際の掲載元URLへ解決できない。
  センチメント判定・日付/場所の確認等はすべて見出し文のみが根拠であり、記事本文には
  基づいていない。
- **真のリアルタイム更新ではない**: GitHub Actionsのcron(30分毎)によるバッチ更新であり、
  GitHub Pagesは静的ホスティングのためサーバー側の常時実行はできない。
- **Formula Drift(米国)・Supercars Championship(豪州)はニュース+リンクのみ**:
  両サイトともサーバー側で実データを描画しているが、その埋め込み方式がNext.jsの内部
  「flight-stream」形式(`self.__next_f.push(...)`)という非公開・非文書化のシリアライズ
  形式であることを確認した(2026-08-22時点)。HTMLテーブルのような安定した構造を持つ
  ドキュメント化された形式ではなく、フレームワークのバージョンアップ等で予告なく変化し
  得るため、誤解析による誤表示リスクを避け、あえて一覧化・グラフ化はせずニュース集約と
  公式サイトへのリンクのみとしている。技術的には抽出可能なデータだが、安定性を優先した
  設計判断であることを明記する。
- **D1GP・SUPER GT GT300のURL/パラメータは変化しうる**: D1GPのランキングページは
  日本語URLエンコードされたスラッグ(`d1gp.co.jp/2026d1グランプリシリーズランキング/`)
  であり、年度が変わるとURLごと変更される可能性が高い。空表示が続く場合は公式サイトの
  ナビゲーションから最新URLを確認し、`scripts/sources/standings.py` の定数を更新する
  こと。SUPER GT GT300の`?gt_class=gt300`パラメータによる絞り込みは2026-08-22時点で
  動作を確認済みだが、サイト側の実装変更で無効化される可能性はある。
- **モータースポーツのGR Supra参戦フラグは推定**: 各シリーズの順位表自体には使用車種が
  掲載されていないため、`standings.py` 内にハードコードしたドライバー名/カー番号リスト
  との一致でハイライト表示している。ドライバー交代等があった場合、リストの更新が追いつか
  ない可能性がある。
- **歴代Supra YouTube(⑤)は世代により情報量に差がある**: A40/A50・A60(1978-1986年、
  国内では「セリカXX」)は現行GRスープラや4代目JZA80と比べ動画自体が少なく、該当セクション
  が薄くなる傾向がある。これは検索クエリの精度問題ではなく、実際の情報流通量の違いによるもの。
- **ライバル車カタログ(②)の生産状況は調査時点(2026年8月)のもの**: 特に以下3車種は
  生産終了/状況が流動的なため、カード内の「生産状況」欄で個別に注記している。
  - **Porsche 718 Cayman**: 2025年10月にガソリンモデルの生産を終了し新規受注も停止。
    電動後継の計画は中止/延期と報じられており、後継の方向性は本記事作成時点で未確定。
  - **Chevrolet Camaro**: 2024年モデルをもって生産終了。GMは2026年前後の復活を発表して
    いるが、ガソリン車か電動SUVかを含め詳細は未確定。
  - **Nissan GT-R**: 世界生産終了(日本を含む全世界向けが2025年8月に終了、米国向けは
    2024年モデルが最終)。次世代モデルの投入が示唆されているが現行モデルは存在しない。
  価格・スペックは為替・オプション・年式により変動するため、あくまで参考値として扱うこと。
- **センチメント判定は見出し文のみの自動推定**: 判定根拠語が1語以下の場合は中立とする
  2語ゲート(英語のみ)により、単語1つで結論が引っ張られる誤判定を抑えている。日本語は
  自動車文脈専用の手作り辞書のため1語一致でも判定を確定している。
- **YouTube検索スクレイピングの脆弱性**: YouTube側のページ構造変更により取得に失敗する
  可能性がある。失敗時はダッシュボード上に取得エラーとして表示される。動画ごとの概要欄
  プレビュー取得は、GitHub Actions共有IPからのボット対策(429エラー)に確実に引っかかる
  ことを確認済みのため実装していない(検索結果ページの取得自体は問題ない)。
- **UI文言の翻訳辞書はapp.js内で一元管理**: `data/latest.json` 側の各セクションは表示用
  ラベルを持たず、`site/app.js` の `I18N` 辞書を section/region/series/generation の
  安定したkeyで参照して日英を出し分けている。新しいセクション/地域/シリーズ/世代を追加
  した場合は、Python側のkeyと `I18N.ja` / `I18N.en` 双方のエントリを対応させること。
- **ライバル車カタログは静的データ**: `site/data/rivals.json` は30分毎の自動更新の対象外
  で、手動収集した参考価格・スペックを元にした静的ファイル(`{ja, en}` 形式のバイリンガル
  データ)。更新する場合は同ファイルを直接編集する。

## 構成

```
scripts/
  fetch_data.py           # 全ソースを集約し site/data/latest.json を生成
  sources/
    common.py              # RSS取得・数値/日時パース等の共通処理
    sentiment.py             # 見出し文からのポジティブ/ネガティブ推定(VADER + 日本語辞書)
    youtube.py                # YouTube検索結果スクレイピング(人気/新着の共通ロジック)
    official_news.py           # ①公式リリース(市販GRスープラ + GT4 + GT500)
    rivals.py                    # ③④共通のライバル車ロースター(車種名・クエリ)
    rival_topics.py                # ③ライバル車トピックス
    rival_youtube.py                 # ④ライバル車YouTube
    historic_youtube.py                # ⑤歴代Supra YouTube(全世代)
    inline_six.py                       # ⑥世界の直列6気筒エンジントピックス
    complaints.py                        # ⑦Supra顧客の声・クレーム
    motorsports.py                        # ⑧地域別モータースポーツ情報集約
    schedule.py                            # ⑧SUPER GT/FDJ/D1GPの年間日程(実データ)
    standings.py                            # ⑧SUPER GT/FDJ/D1GPのランキング(実データ)
site/
  index.html / style.css / app.js   # ダッシュボード本体(静的サイト)
  data/latest.json                  # 自動生成される最新データ(コミット対象外)
  data/rivals.json                  # ②ライバル車カタログ(手動更新・コミット対象)
.github/workflows/update-dashboard.yml  # 30分毎の自動更新 + GitHub Pagesデプロイ
```

## ローカルでの動作確認

```bash
cd scripts
pip install -r requirements.txt
python fetch_data.py          # site/data/latest.json を生成
cd ../site
python3 -m http.server 8000   # http://localhost:8000 で確認
```

## GitHub Pagesの有効化(初回のみ)

リポジトリの Settings > Pages > Build and deployment > Source を
**GitHub Actions** に設定する。設定後、`update-dashboard` ワークフローの実行(スケジュール
または手動の workflow_dispatch)によって自動的に公開される。
