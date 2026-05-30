import json, urllib.request, os

SUPABASE_URL = "https://cbxipgqfhbsmgmatherr.supabase.co"
# 読み取り専用のエクスポートなので anon キーで OK
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNieGlwZ3FmaGJzbWdtYXRoZXJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNDMwMzcsImV4cCI6MjA4OTkxOTAzN30.Q1tuMpTsuhCPDAWLUohDI6PTDPZNZU8Uxwf30ENHmNI"

def fetch_all(table, select="*", order="name.asc"):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={select}&limit=10000&order={order}"
    req = urllib.request.Request(url, headers={
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}"
    })
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))

os.makedirs("data", exist_ok=True)

# ── kaiju ──────────────────────────────────────────
print("▶ kaiju をエクスポート中...")
try:
    kaiju = fetch_all("kaiju")
    with open("data/kaiju.json", "w", encoding="utf-8") as f:
        json.dump(kaiju, f, ensure_ascii=False, indent=2)
    print(f"  完了: {len(kaiju)}件 → data/kaiju.json")
except Exception as e:
    print(f"  エラー: {e}")

# ── ultraman + moves（moves を各ウルトラマンに埋め込む）──
print("▶ ultraman をエクスポート中...")
try:
    ultraman = fetch_all("ultraman")
    moves    = fetch_all("ultraman_moves")

    moves_by_id = {}
    for m in moves:
        uid = m["ultraman_id"]
        moves_by_id.setdefault(uid, []).append(m)

    for um in ultraman:
        um["moves"] = sorted(
            moves_by_id.get(um["id"], []),
            key=lambda m: m.get("order_no", 0)
        )

    with open("data/ultraman.json", "w", encoding="utf-8") as f:
        json.dump(ultraman, f, ensure_ascii=False, indent=2)
    print(f"  完了: {len(ultraman)}件（技 {len(moves)}件含む）→ data/ultraman.json")
except Exception as e:
    print(f"  エラー（ultramanテーブル未作成の場合は正常）: {e}")
    # 空ファイルを作成しておく
    for path in ["data/ultraman.json"]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f)

print("\n✅ エクスポート完了")
