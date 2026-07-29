#!/usr/bin/env python3
"""
怪獣データ追加スクリプト
使い方: python3 tools/add_series.py <シリーズ名> <JSONファイルパス>

例: python3 tools/add_series.py ウルトラマンゼット /tmp/kaiju_new.json
"""
import json
import sys

def main():
    if len(sys.argv) < 3:
        print("使い方: python3 tools/add_series.py <シリーズ名> <JSONファイルパス>")
        sys.exit(1)

    series = sys.argv[1]
    json_path = sys.argv[2]

    with open('data/kaiju.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)

    with open(json_path, 'r', encoding='utf-8') as f:
        new_entries = json.load(f)

    existing_keys = {(x['name'], x.get('series')) for x in existing}

    added, skipped = [], []
    for entry in new_entries:
        entry['series'] = series
        # 必須フィールドのデフォルト補完
        entry.setdefault('tc', 'r')
        entry.setdefault('tags', entry.get('type', ''))
        entry.setdefault('origin', '不明')
        entry.setdefault('height', '不明')
        entry.setdefault('weight', '不明')
        entry.setdefault('desc', '')

        key = (entry['name'], series)
        if key not in existing_keys:
            existing.append(entry)
            existing_keys.add(key)
            added.append(entry['name'])
        else:
            skipped.append(entry['name'])

    with open('data/kaiju.json', 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, separators=(',', ':'))

    print(f"シリーズ: {series}")
    print(f"追加: {len(added)}件 / スキップ（重複）: {len(skipped)}件 / 合計: {len(existing)}件")
    if added:
        for n in added:
            print(f"  + {n}")
    if skipped:
        print(f"  スキップ: {', '.join(skipped)}")

if __name__ == '__main__':
    main()
