# SPEC-003: ウルトラシリーズ最新ニュース自動取得・表示

## 参照企画書
docs/planning/PLAN-003.md

---

## アーキテクチャ

```
GitHub Actions (毎日 2:00 AM JST)
    └─ python tools/fetch_news.py
         ├─ Google News RSS: "ウルトラマン 円谷"（Yahoo!ニュース・円谷公式カバー）
         └─ Google News RSS: "プレミアムバンダイ ウルトラ"（プレバン関連カバー）
              ↓ フィルタリング・重複除去・最新10件
         data/news.json へ書き込み
         git commit & push
              ↓
index.html が fetch('data/news.json') して表示
```

**なぜGoogle News RSS一本か:**
- m78.jp（円谷公式）は403 Forbidden、p-bandai.jp はスクレイピング不可
- Google News RSSは Yahoo!ニュース記事を出典元として含む（実データで確認）
- 円谷プロ公式リリースも Google News 経由で流れることを確認

---

## 変更対象ファイル

| ファイル | 種別 | 内容 |
|----------|------|------|
| `tools/fetch_news.py` | 新規作成 | ニュース取得スクリプト |
| `.github/workflows/fetch_news.yml` | 新規作成 | GitHub Actions cron 設定 |
| `data/news.json` | 新規作成（自動生成） | ニュースデータ |
| `index.html` | 既存変更 | ニュース表示セクション追加 |

---

## tools/fetch_news.py の仕様

### 取得クエリ

| クエリ | 狙い |
|--------|------|
| `ウルトラマン 円谷` | 円谷公式リリース・Yahoo!ニュース全般 |
| `プレミアムバンダイ ウルトラ` | プレバン限定商品情報 |

### RSS URL

```
https://news.google.com/rss/search?q={query}&hl=ja&gl=JP&ceid=JP:ja
```

### フィルタリングロジック

**除外条件（ノイズ除去）:**
- タイトルにウルトラ系キーワードを含まないもの
- 対象キーワード: `ウルトラマン|ウルトラ怪獣|ウルトラセブン|ウルトラシリーズ|円谷|プレバン.*ウルトラ|ウルトラ.*プレバン`

**含める出典優先度:**
1. 円谷プロ公式 (`m78.jp` を含む URL)
2. Yahoo!ニュース
3. 電撃ホビー・hobby watch・アニメイト（プレバン商品情報）
4. その他

**重複除去:** URL の正規化後に set で dedup

**件数:** 最新10件（日付降順）

### data/news.json スキーマ

```json
[
  {
    "date": "2026-06-17",
    "title": "60周年記念「ULTRA SUMMER in IKEBUKURO」開催",
    "url": "https://m78.jp/news/...",
    "source": "円谷プロ公式"
  }
]
```

| フィールド | 型 | 説明 |
|-----------|---|------|
| date | string (YYYY-MM-DD) | 記事公開日 |
| title | string | 記事タイトル（Google News からそのまま取得） |
| url | string | 元記事URL（Google Newsリダイレクトを解決） |
| source | string | 出典名（フィード entry の source.title） |

### エラーハンドリング

- ネットワークエラー時は既存の `data/news.json` を維持（上書きしない）
- 取得件数が0件の場合も既存ファイルを維持

---

## .github/workflows/fetch_news.yml の仕様

```yaml
name: ニュース自動更新
on:
  schedule:
    - cron: '0 17 * * *'   # 毎日 2:00 AM JST (UTC+9)
  workflow_dispatch:        # 手動実行ボタン（テスト用）

jobs:
  fetch:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install feedparser requests
      - run: python tools/fetch_news.py
      - name: 変更があればコミット
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/news.json
          git diff --staged --quiet || (
            git commit -m "🔄 ニュース自動更新 $(date +'%Y-%m-%d')" &&
            git push
          )
```

**ポイント:**
- `permissions: contents: write` で `GITHUB_TOKEN` による push を許可
- `workflow_dispatch` で即時手動テスト可能
- 変更がない日はコミットしない（`git diff --staged --quiet`）

---

## index.html の変更

### 挿入位置

search-block の終わりとシリーズグリッドの間（`#p-search` パネル内）。

### 追加HTML

```html
<div class="news-section" id="news-section">
  <div class="news-heading">最新情報</div>
  <ul class="news-list" id="news-list">
    <li class="news-loading">読み込み中…</li>
  </ul>
</div>
```

### 追加CSS

```css
.news-section { margin-top: 20px; margin-bottom: 0;
  border: 1px solid #c0a070; background: #fffdf7; }
.news-heading { ... }   /* 既存スタイルに合わせた見出し */
.news-list { list-style: none; }
.news-item { ... }      /* 日付 + タイトル + 出典 の1行 */
.news-item a { ... }    /* 外部リンク（別タブ） */
```

### 追加JS

ページロード時に `data/news.json` を fetch してリストを描画。
`loadSeriesList()` と同タイミングで呼び出す。

```javascript
async function loadNews() {
  try {
    const res = await fetch('data/news.json');
    const news = await res.json();
    const list = document.getElementById('news-list');
    if (!news.length) { /* 非表示 */ return; }
    list.innerHTML = news.map(n => `
      <li class="news-item">
        <span class="news-date">${n.date}</span>
        <a href="${n.url}" target="_blank" rel="noopener">${n.title}</a>
        <span class="news-source">${n.source}</span>
      </li>
    `).join('');
  } catch(e) { /* news-section を非表示 */ }
}
```

### ニュースがゼロ件の場合
`#news-section` を非表示にする（検索フォームの見た目を壊さない）。

---

## 受け入れ条件

- [ ] `tools/fetch_news.py` を手動実行すると `data/news.json` が生成される
- [ ] JSON に date / title / url / source が含まれる
- [ ] 重複記事が除去されている
- [ ] ウルトラ系に無関係な記事が含まれない
- [ ] GitHub Actions workflow ファイルが存在し、cron スケジュールが設定されている
- [ ] index.html のニュース欄に最新情報が表示される
- [ ] 日付・タイトル・出典名が表示される
- [ ] タイトルクリックで外部リンクが別タブで開く
- [ ] ニュースが0件の場合はセクションが非表示になる
- [ ] `workflow_dispatch` で手動実行してデータ更新を確認できる

---
ステータス: ✅ 実装完了
作成日: 2026-06-17
