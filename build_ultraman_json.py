"""
upload_ultraman.py のデータを data/ultraman.json に変換するスクリプト
新しいウルトラマンを追加したいときは upload_ultraman.py にデータを足してから
このスクリプトを実行してください
"""
import json, sys
sys.path.insert(0, '.')
from upload_ultraman import ultraman_rows, moves_by_name

result = []
for i, um in enumerate(ultraman_rows, start=1):
    entry = {**um, "id": i}
    entry["moves"] = [
        {**m, "id": (i - 1) * 10 + m["order_no"], "ultraman_id": i}
        for m in moves_by_name.get(um["name"], [])
    ]
    result.append(entry)

with open("data/ultraman.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✅ {len(result)}件 → data/ultraman.json")
for um in result:
    print(f"  [{um['id']}] {um['name']}（技 {len(um['moves'])}件）")
