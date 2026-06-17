"""
ウルトラシリーズ関連ニュースを Google News RSS から取得し data/news.json に保存する。
GitHub Actions から毎日 2:00 AM JST に実行される。
"""
import feedparser
import json
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_FILE = ROOT / "data" / "news.json"

QUERIES = [
    "ウルトラマン 円谷",
    "ウルトラシリーズ 新作",
]

ULTRA_RE = re.compile(
    r'ウルトラマン|ウルトラ怪獣|ウルトラセブン|ウルトラシリーズ|円谷|'
    r'ティガ|ダイナ|ガイア|コスモス|メビウス|ゼロ|ギンガ|エックス|オーブ|ジード|'
    r'トリガー|デッカー|ブレーザー|アーク|ULTRAMAN'
)

MAX_ITEMS = 10


def strip_source_suffix(title: str) -> str:
    """タイトル末尾の出典名を除去する。
    - Google News形式:  「タイトル - 出典名」
    - Yahoo形式:        「タイトル（出典名）」または「タイトル（出典名」
    - Livedoor形式:     「タイトル (YYYY年M月D日掲載)」
    ただし「（前・後編）」のような本文中の括弧は除去しない。
    """
    # " - 出典名" を除去
    title = re.sub(r'\s+[-–—]\s+[^-–—]{2,30}$', '', title).strip()
    # 「（出典名）」「（出典名」「(出典名)」を除去（・や、を含む場合は本文扱いで残す）
    title = re.sub(r'[（(][^）)（(・、。]{2,30}[）)]?\s*$', '', title).strip()
    return title


def get_source(entry) -> str:
    src = entry.get('source', {})
    if isinstance(src, dict):
        return src.get('title', '')
    return ''


def parse_dt(entry) -> datetime:
    if entry.get('published_parsed'):
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def normalize_title(title: str) -> str:
    """重複判定用にタイトルを正規化する（記号・空白を除いた先頭30文字）"""
    return re.sub(r'[^\w]', '', title)[:30]


def main():
    seen_urls = set()
    seen_titles = set()
    items = []

    for query in QUERIES:
        url = (
            'https://news.google.com/rss/search?q='
            + urllib.parse.quote(query)
            + '&hl=ja&gl=JP&ceid=JP:ja'
        )
        try:
            feed = feedparser.parse(url)
            print(f'  [{query}] {len(feed.entries)}件取得')
        except Exception as e:
            print(f'Warning: {query} → {e}')
            continue

        for entry in feed.entries:
            raw_title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            if not raw_title or not link:
                continue
            if not ULTRA_RE.search(raw_title):
                continue

            title = strip_source_suffix(raw_title)
            title_key = normalize_title(title)

            # URL重複 or タイトル重複（同記事が複数ソース経由で流れる場合）を除外
            if link in seen_urls or title_key in seen_titles:
                continue
            seen_urls.add(link)
            seen_titles.add(title_key)

            items.append({
                'date': parse_dt(entry).strftime('%Y-%m-%d'),
                'title': title,
                'url': link,
                'source': get_source(entry),
                '_dt': parse_dt(entry),
            })

    if not items:
        print('取得件数0件 — 既存ファイルを維持します。')
        return

    items.sort(key=lambda x: x['_dt'], reverse=True)

    result = [
        {'date': x['date'], 'title': x['title'], 'url': x['url'], 'source': x['source']}
        for x in items[:MAX_ITEMS]
    ]

    OUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'✅ {len(result)}件 → {OUT_FILE}')
    for r in result:
        print(f"  [{r['date']}] [{r['source']}] {r['title'][:55]}")


if __name__ == '__main__':
    main()
