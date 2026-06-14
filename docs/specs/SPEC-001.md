# SPEC-001: 検索結果ページの独立

## 参照企画書
docs/planning/PLAN-001.md

---

## 変更対象ファイル

| ファイル | 種別 | 変更内容 |
|----------|------|----------|
| `index.html` | 既存変更 | 結果エリア削除・doSearch() をページ遷移に変更 |
| `search_result.html` | 新規作成 | 検索結果専用ページ |

---

## index.html の変更

### 削除するHTML要素（`#p-search` パネル内）

```html
<!-- 以下をすべて削除 -->
<div id="result-bar" class="result-bar hid">…</div>
<div id="d-box" class="hid"></div>
<div id="s-loading" class="loading hid">…</div>
<div id="s-empty" class="empty hid">…</div>
<div id="s-init" class="empty">…</div>
<div id="k-grid" class="kaiju-grid"></div>
```

### 削除するJS関数

以下の関数は `search_result.html` 側に移動するため `index.html` からは削除：

- `fetchFromDB()`
- `renderGrid()`
- `showDetail()`
- `applySort()`
- `sortBy()`
- `setLoading()` / `show()` / `hide()`（検索結果用途分）
- `toggleFav()` / `toggleFavDetail()`（検索結果カード用）

※ `loadKaijuDB()`・`loadSeriesList()`・`tab()`・お気に入り系・クイズ系は残す。

### 変更するJS関数: `doSearch()`

```javascript
function doSearch() {
  const qName = document.getElementById('si-name').value.trim();
  const qAlias = document.getElementById('si-alias').value.trim();
  const qEp = document.getElementById('ep-num').value.trim();
  const qSeries = document.getElementById('series-select').value;
  if (!qName && !qAlias && !qEp && qSeries === 'all') return;
  const p = new URLSearchParams();
  if (qName) p.set('name', qName);
  if (qAlias) p.set('alias', qAlias);
  if (qEp) p.set('ep', qEp);
  if (qSeries !== 'all') p.set('series', qSeries);
  window.location.href = 'search_result.html?' + p.toString();
}
```

### 変更するJS関数: `filterS()`

シリーズ変更時のインライン検索を廃止。選択状態の保持のみ行う：

```javascript
function filterS(el) {
  curSeries = el.value;
}
```

### Enterキー対応

検索入力フィールドに `keydown` イベントを追加し、Enter で `doSearch()` を呼ぶ：

```javascript
document.querySelectorAll('.search-input, .ep-input').forEach(el => {
  el.addEventListener('keydown', e => { if (e.key === 'Enter') doSearch(); });
});
```

### 削除するCSS

index.html 内の `<style>` から、結果表示にしか使わないクラスを削除：

- `.kaiju-grid`
- `.kcard` 系（`.kcard`, `.kcard-num`, `.kcard-name`, `.kcard-series`, `.kcard-desc`, `.kcard-tags`）
- `.result-bar`, `.result-count`, `.sort-row`, `.sort-btn`
- `.detail-box`, `.detail-name`, `.detail-series`, `.detail-stats`, `.detail-body`, `.detail-close`, `.detail-fav`, `.stat` 系
- `.fav-btn`
- `.loading`, `.dot`
- `.empty`
- `.hid`

※ お気に入り・クイズで使うクラスは残す。`#fav-grid` で `.kaiju-grid` `.kcard` 系を使っているため、お気に入りパネルで流用している分は残す必要あり → **お気に入りパネルも `search_result.html` と同じCSSを参照するか、index.html に必要分を残す。**

**判断:** kcard系CSSはお気に入りパネルでも使うため index.html に残す。result-bar/detail/loading/hid 系は search_result.html 側に移す。

---

## search_result.html の新規作成

### URLパラメータ仕様

| パラメータ | 型 | 説明 | 例 |
|-----------|---|------|---|
| `name` | string | 怪獣名キーワード（部分一致） | `name=ゴモラ` |
| `alias` | string | 別名・タグキーワード（部分一致） | `alias=電気怪獣` |
| `series` | string | シリーズ名（完全一致） | `series=ウルトラセブン` |
| `ep` | number | 話数（完全一致） | `ep=1` |

### ページ構成

```
[ヘッダー] ← index.html と同一デザイン
[ナビ]     ← 怪獣検索リンク（← 検索に戻る）/ クイズ / お気に入り / ウルトラマン
[検索条件バナー] ← 現在の検索条件を表示（例:「ウルトラセブン の怪獣 · 7件」）
[ソートバー]     ← 名前順 / シリーズ順 / 登場話順
[怪獣グリッド]   ← kcard 一覧
[詳細モーダル]   ← kcard クリックで展開（index.html と同じ）
[0件時メッセージ]
```

### ナビの「← 検索に戻る」挙動

- クリックで `index.html` へ戻る（URLパラメータは引き継がない）
- ブラウザ戻るボタンでも `index.html` の状態に戻る（自然な履歴）

### お気に入り機能

- `search_result.html` 上でも ★ ボタンを表示・操作可能（localStorage を使用）
- index.html と同じ `isFav` / `saveFavs` ロジックを持つ

---

## 受け入れ条件

- [ ] index.html の検索ボタンを押すと `search_result.html` に遷移する
- [ ] URLに検索条件がパラメータとして含まれる（例: `?name=ゴモラ&series=ウルトラセブン`）
- [ ] search_result.html でURLパラメータから検索条件を復元し、自動で結果を表示する
- [ ] 「← 検索に戻る」で index.html に戻れる
- [ ] 0件の場合は「該当する怪獣が見つかりませんでした」を表示する
- [ ] ソート（名前順・シリーズ順・登場話順）が機能する
- [ ] 怪獣カードクリックで詳細モーダルが開く
- [ ] お気に入り追加・解除が機能する
- [ ] デザインが index.html と統一されている
- [ ] Enterキーで検索実行できる（index.html）

---
ステータス: ✅ 実装完了
作成日: 2026-06-15
