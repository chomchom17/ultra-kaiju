import json, urllib.request, os, re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
CLAUDE_MD = ROOT / "CLAUDE.md"

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

def normalize_episode(ep: str) -> str:
    """第N話・第M話 → 第N・M話 に正規化する。"""
    if re.match(r'^第\d+話(?:・第\d+話)+$', ep):
        nums = re.findall(r'\d+', ep)
        return '第' + '・'.join(nums) + '話'
    return ep

def update_claude_md(kaiju: list):
    """CLAUDE.md の <!-- auto-series-start/end --> 区間をシリーズ件数で書き換える。"""
    text = CLAUDE_MD.read_text(encoding="utf-8")

    counts = Counter(k["series"] for k in kaiju)
    total = sum(counts.values())
    lines = [f"- {s}: {c}件" for s, c in sorted(counts.items(), key=lambda x: -x[1])]
    block = "\n".join(lines)

    # ヘッダー行の合計件数を更新
    text = re.sub(
        r'### シリーズ別件数（合計\d+件）',
        f'### シリーズ別件数（合計{total}件）',
        text
    )
    # マーカー間の内容を置換
    text = re.sub(
        r'<!-- auto-series-start -->.*?<!-- auto-series-end -->',
        f'<!-- auto-series-start -->\n{block}\n<!-- auto-series-end -->',
        text,
        flags=re.DOTALL
    )
    # プロジェクト概要と構成図の件数も更新
    text = re.sub(r'`data/kaiju\.json`（\d+件）', f'`data/kaiju.json`（{total}件）', text)
    text = re.sub(r'kaiju\.json\s+怪獣データ（\d+件）', f'kaiju.json          怪獣データ（{total}件）', text)

    CLAUDE_MD.write_text(text, encoding="utf-8")
    print(f"  CLAUDE.md を更新: 合計{total}件 / {len(counts)}シリーズ")

DATA_DIR.mkdir(exist_ok=True)

# ── kaiju ──────────────────────────────────────────
print("▶ kaiju をエクスポート中...")
try:
    kaiju = fetch_all("kaiju")
    for k in kaiju:
        if k.get("episode"):
            k["episode"] = normalize_episode(k["episode"])
    with open(DATA_DIR / "kaiju.json", "w", encoding="utf-8") as f:
        json.dump(kaiju, f, ensure_ascii=False, separators=(',', ':'))
    print(f"  完了: {len(kaiju)}件 → {DATA_DIR}/kaiju.json")
    update_claude_md(kaiju)
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

    with open(DATA_DIR / "ultraman.json", "w", encoding="utf-8") as f:
        json.dump(ultraman, f, ensure_ascii=False, indent=2)
    print(f"  完了: {len(ultraman)}件（技 {len(moves)}件含む）→ {DATA_DIR}/ultraman.json")
except Exception as e:
    print(f"  エラー（ultramanテーブル未作成の場合は正常）: {e}")
    # 空ファイルを作成しておく
    out = DATA_DIR / "ultraman.json"
    if not out.exists():
        with open(out, "w", encoding="utf-8") as f:
            json.dump([], f)

print("\n✅ エクスポート完了")
