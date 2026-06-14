# ウルトラ怪獣大図鑑 — CLAUDE.md

## プロジェクト概要

ウルトラシリーズ（初代〜）の怪獣・宇宙人をまとめた静的Webアプリ図鑑。
テキスト検索・シリーズ絞り込み・話数検索・ウルトラマン一覧閲覧ができる。

- **フロントエンド**: 素のHTML/CSS/JS（フレームワークなし）
- **データ**: `data/kaiju.json`（505件）、`data/ultraman.json`（ウルトラ戦士）
- **バックエンド**: Supabase（Postgres）— データ更新時のみ使用
- **公開形式**: 静的HTML（ビルド不要、index.htmlを直接開ける）

## ディレクトリ構成

```
ultra-kaiju/
├── CLAUDE.md               このファイル
├── index.html              メイン画面（怪獣図鑑・検索）
├── ultraman_list.html      ウルトラ戦士一覧
├── ultraman_detail.html    ウルトラ戦士詳細
├── data/
│   ├── kaiju.json          怪獣データ（505件）
│   ├── ultraman.json       ウルトラ戦士データ
│   └── kaiju_data_v3.csv   元データCSV（参照用）
├── tools/                  管理スクリプト（Python）
│   ├── export_to_json.py   Supabase → data/*.json エクスポート
│   ├── build_ultraman_json.py  upload_ultraman.py → ultraman.json ビルド
│   ├── upload_ultraman.py  ウルトラ戦士マスターデータ
│   └── upload_neos.py      ネオス系データアップロード
├── db/                     DB定義SQL
├── docs/                   企画・仕様・設計ドキュメント（エージェント間引き継ぎ）
│   ├── workflow.md         運用フロー定義
│   ├── planning/           企画書（PLAN-NNN.md）
│   ├── specs/              仕様書（SPEC-NNN.md）
│   └── designs/            デザイン案（DESIGN-NNN.md）
└── archive/                旧バージョンファイル
```

## データ構造

### kaiju.json フィールド

| フィールド | 型 | 説明 |
|---|---|---|
| name | string | 怪獣名（表示名） |
| series | string | 作品名（例: 「初代ウルトラマン」「ウルトラセブン」） |
| type | string | 種別（怪獣 / 宇宙人 / ロボット怪獣 など） |
| origin | string | 出身地・出現場所 |
| height | string | 身長（例: 「60m」「15〜180m」） |
| weight | string | 体重（例: 「2万5千t」） |
| desc | string | 怪獣の説明文 |
| episode | string | 登場話（例: 「第1話」「第3・4話」） |
| episode_name | string | 話のタイトル |
| tc | string | タイムコード区分（r=赤/g=緑/blue） |
| tags | string | 怪獣の特徴タグ（例: 「凶暴怪獣」「円盤生物」） |

### シリーズ別件数（合計505件）

- ザ・ウルトラマン: 66件
- ウルトラセブン: 63件
- ウルトラマン80: 63件
- ウルトラマンタロウ: 58件
- 帰ってきたウルトラマン: 55件
- ウルトラマンレオ: 54件
- 初代ウルトラマン: 51件
- ウルトラマンA: 47件
- ウルトラマンパワード: 18件
- ウルトラマングレート: 15件
- ウルトラマンネオス: 15件

## 運用フロー（マルチエージェント）

**オーナー（masaomi）の役割:**
- 改善インプットを提供する
- 企画・仕様・デザイン案をレビュー・承認する
- 実装後の動作確認・フィードバックを行う

**エージェントの役割（以下以外はすべてエージェントが担う）:**
- 企画フェーズ: `docs/planning/PLAN-NNN.md` を作成
- 仕様フェーズ: `docs/specs/SPEC-NNN.md` を作成
- デザインフェーズ: `docs/designs/DESIGN-NNN.md` を作成
- 実装フェーズ: コード変更・commit・push

詳細フローは [docs/workflow.md](docs/workflow.md) を参照。

## 技術方針・注意事項

- **ビルド不要**: HTMLファイルは直接編集・確認できる
- **データ更新**: `data/kaiju.json` を直接編集するか `python3 tools/export_to_json.py` でSupabaseから再取得
- **Supabase操作**: 本番DBへの直接操作は慎重に行うこと。読み取りはanon keyで可
- **CSS**: インラインスタイル（`<style>`タグ内）で管理。外部CSSファイルなし
- **JS**: インラインスクリプト（`<script>`タグ内）で管理。外部JSファイルなし
- **文字コード**: UTF-8、日本語コメント・変数名OK
- **コミット**: 修正・追加後は自動でcommit & pushまで行う

## スクリプト実行方法

```bash
# Supabaseからデータ再取得（ルートから実行）
python3 tools/export_to_json.py

# ウルトラマンデータをJSONビルド（ルートから実行）
python3 tools/build_ultraman_json.py

# ローカル確認用サーバー
python3 -m http.server 18741
```
