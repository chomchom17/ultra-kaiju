#!/usr/bin/env python3
"""
怪獣データ追加スクリプト
使い方: python3 tools/add_series.py <シリーズ名> <JSONファイルパス> [--year <放送開始年>]

例: python3 tools/add_series.py ウルトラマンジード /tmp/kaiju_new.json --year 2017
"""
import json
import sys
import re
import argparse

HTML_PATH = 'index.html'


def update_html_series(series_name, year):
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    order_match = re.search(r"const SERIES_ORDER = \[(.*?)\];", content)
    year_match = re.search(r"const SERIES_YEAR = \{(.*?)\};", content)
    if not order_match or not year_match:
        print("警告: index.html の SERIES_ORDER/SERIES_YEAR が見つかりません")
        return

    current_order = [s.strip().strip("'\"") for s in order_match.group(1).split(',') if s.strip()]

    current_years = {}
    for item in year_match.group(1).split(','):
        item = item.strip()
        if ':' in item:
            k, v = item.rsplit(':', 1)
            k = k.strip().strip("'\"")
            try:
                current_years[k] = int(v.strip())
            except ValueError:
                pass

    if series_name not in current_order:
        current_order.append(series_name)
    current_years[series_name] = year

    current_order.sort(key=lambda s: (current_years.get(s, 9999), s))

    new_order_str = ','.join(f"'{s}'" for s in current_order)
    new_year_items = sorted(current_years.items(), key=lambda x: (x[1], x[0]))
    new_year_str = ','.join(f"'{k}':{v}" for k, v in new_year_items)

    content = re.sub(r"const SERIES_ORDER = \[.*?\];", f"const SERIES_ORDER = [{new_order_str}];", content)
    content = re.sub(r"const SERIES_YEAR = \{.*?\};", f"const SERIES_YEAR = {{{new_year_str}}};", content)

    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"index.html を更新しました: {series_name} ({year}年) を追加・並び順を調整")


def main():
    parser = argparse.ArgumentParser(description='怪獣データ追加スクリプト')
    parser.add_argument('series', help='シリーズ名')
    parser.add_argument('json_path', help='JSONファイルパス')
    parser.add_argument('--year', type=int, help='放送開始年（例: 2017）')
    args = parser.parse_args()

    with open('data/kaiju.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)

    with open(args.json_path, 'r', encoding='utf-8') as f:
        new_entries = json.load(f)

    existing_keys = {(x['name'], x.get('series')) for x in existing}

    added, skipped = [], []
    for entry in new_entries:
        entry['series'] = args.series
        entry.setdefault('tc', 'r')
        entry.setdefault('tags', entry.get('type', ''))
        entry.setdefault('origin', '不明')
        entry.setdefault('height', '不明')
        entry.setdefault('weight', '不明')
        entry.setdefault('desc', '')

        key = (entry['name'], args.series)
        if key not in existing_keys:
            existing.append(entry)
            existing_keys.add(key)
            added.append(entry['name'])
        else:
            skipped.append(entry['name'])

    with open('data/kaiju.json', 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, separators=(',', ':'))

    print(f"シリーズ: {args.series}")
    print(f"追加: {len(added)}件 / スキップ（重複）: {len(skipped)}件 / 合計: {len(existing)}件")
    if added:
        for n in added:
            print(f"  + {n}")
    if skipped:
        print(f"  スキップ: {', '.join(skipped)}")

    if args.year:
        update_html_series(args.series, args.year)
    else:
        print(f"注意: --year を指定すると index.html の並び順・放送年が自動更新されます")
        print(f"例: python3 tools/add_series.py {args.series} {args.json_path} --year YYYY")


if __name__ == '__main__':
    main()
