# SPEC-002: シリーズ入口ボタン（A-1）＋ 怪獣詳細専用ページ（B-1）

## 参照企画書
docs/planning/PLAN-002.md（A-1、B-1）

---

## 変更対象ファイル

| ファイル | 種別 | 変更内容 |
|----------|------|----------|
| `index.html` | 既存変更 | 検索フォーム下にシリーズグリッドを追加 |
| `search_result.html` | 既存変更 | カードクリックを詳細ページ遷移に変更・モーダル削除 |
| `kaiju_detail.html` | 新規作成 | 怪獣詳細専用ページ |

---

## A-1: index.html — シリーズ入口グリッド

### 追加HTML（search-block の直後）

```html
<div class="browse-section">
  <div class="browse-heading">シリーズから探す</div>
  <div class="series-grid" id="series-grid"></div>
</div>
```

### 追加CSS

```css
.browse-section { margin-top: 20px }
.browse-heading { font-size:11px; ... }  /* セクション見出し */
.series-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(190px,1fr)); gap:8px }
.series-card { /* ボタン形式。kcard に近いスタイル */ }
.series-card-name { /* シリーズ名 */ }
.series-card-count { /* 「51体」など件数 */ }
```

### 追加JS

`loadSeriesList()` を拡張し、シリーズ別件数を集計してグリッドに描画する。

```javascript
// series-grid を series ごとの件数で生成
data.forEach(k => { counts[k.series] = (counts[k.series] || 0) + 1; });
series.forEach(s => {
  grid.innerHTML += `<a class="series-card" href="search_result.html?series=${encodeURIComponent(s)}">
    <div class="series-card-name">${s}</div>
    <div class="series-card-count">${counts[s]}体</div>
  </a>`;
});
```

---

## B-1: search_result.html — モーダル廃止・詳細ページ遷移化

### 変更点

- カードクリック時: `showDetail()` 呼び出し → `kaiju_detail.html?name=XXX` へ遷移
- 削除: `#d-box` HTML
- 削除: `showDetail()` 関数
- 削除: `toggleFavDetail()` 関数
- 削除: `.detail-box`・`.detail-*`・`.stat` 系 CSS

### ★ボタン（お気に入り）の扱い

カード上の ★ ボタンは引き続きインラインで動作（`toggleFav()`）。詳細ページ遷移は不要。

---

## B-1: kaiju_detail.html — 新規作成

### URLパラメータ

`?name=ゴモラ`（怪獣名で完全一致検索）

### ページ構成

```
[ヘッダー] ← 他ページと同一
[ナビ]     ← search_result.html と同じリンク構成
[← 検索結果に戻る] ボタン（history.back()）
[怪獣詳細ボックス]
  - 怪獣名（大）
  - シリーズ / 登場話 / 話タイトル
  - スタット（身長・体重・出身地）
  - 説明文（全文）
  - 別名・種別タグ
  - ★ お気に入りボタン
[見つからない場合のメッセージ]
```

### JS処理

1. `?name=` パラメータ取得
2. `data/kaiju.json` をフェッチして name で検索
3. 見つかれば全フィールドを描画、`document.title` を更新
4. 見つからなければ「見つかりませんでした」表示

### お気に入り

`localStorage` の `kaiju_favs` を直接読み書き。詳細ページ単体でお気に入り追加・解除可能。

---

## 受け入れ条件

- [ ] index.html のシリーズグリッドに全11シリーズが表示され、クリックで検索結果ページへ遷移する
- [ ] 各シリーズボタンに件数（「51体」など）が表示される
- [ ] search_result.html でカードをクリックすると `kaiju_detail.html?name=XXX` へ遷移する
- [ ] kaiju_detail.html で怪獣名・シリーズ・身長・体重・出身地・説明文・タグが表示される
- [ ] `← 検索結果に戻る` でブラウザ履歴を戻れる
- [ ] kaiju_detail.html 上でお気に入り追加・解除が機能する
- [ ] 直接URLアクセスで怪獣が見つからない場合、エラーメッセージを表示する

---
ステータス: ✅ 実装完了
作成日: 2026-06-17
