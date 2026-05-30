import json, urllib.request

SUPABASE_URL = "https://cbxipgqfhbsmgmatherr.supabase.co"
# service_role キーを使用（Supabase ダッシュボード → Settings → API → service_role）
# このキーはここにのみ記載し、HTML には絶対に書かないこと
SERVICE_ROLE_KEY = "ここにservice_roleキーを貼り付ける"

# ================================================================
# ウルトラマン基本情報
# ================================================================
ultraman_rows = [
    {
        "name": "ウルトラマン",
        "alias": "ハヤタ・シン（科学特捜隊 隊員）",
        "series": "ウルトラマン",
        "series_year": "1966年",
        "height": "40m",
        "weight": "35,000t",
        "age": "20,000歳",
        "flight_speed": "マッハ5",
        "run_speed": "時速450km",
        "origin": "M78星雲 光の国",
        "color_timer": "あり（残り3分で赤く点滅）",
        "type": None,
        "description": "宇宙の警備員として地球を訪れ、怪獣・宇宙人の脅威から地球を守った初代ウルトラ戦士。M78星雲・光の国出身で、地球人のハヤタ・シンに変身能力を与え一体化した。カラータイマーが点滅する3分間の制限時間内に戦いを終わらせなければならない宿命を背負いながら、数多の怪獣を退けた。正義と勇気の象徴として、後のウルトラ戦士たちに多大な影響を与え続けている光の巨人。",
        "image_url": None
    },
    {
        "name": "ウルトラセブン",
        "alias": "モロボシ・ダン（ウルトラ警備隊 隊員）",
        "series": "ウルトラセブン",
        "series_year": "1967年",
        "height": "40m",
        "weight": "35,000t",
        "age": "19,000歳",
        "flight_speed": "マッハ7",
        "run_speed": "時速780km",
        "origin": "M78星雲 光の国",
        "color_timer": "なし（ビームランプで体力を把握）",
        "type": None,
        "description": "M78星雲の宇宙警備員で、宇宙人による地球侵略を阻止するために地球へやって来た。地球人・モロボシ・ダンの姿に化けてウルトラ警備隊に加わり活躍。頭部のアイスラッガーとエメリウム光線を主要武器とし、知性と強力な戦闘力を兼ね備えたウルトラ戦士。後のシリーズでも度々登場し、息子・ウルトラマンゼロを持つウルトラ一族の重要な存在。",
        "image_url": None
    },
    {
        "name": "ウルトラマンジャック",
        "alias": "郷 秀樹（MAT 隊員）",
        "series": "帰ってきたウルトラマン",
        "series_year": "1971年",
        "height": "45m",
        "weight": "45,000t",
        "age": "27,000歳",
        "flight_speed": "マッハ5",
        "run_speed": "時速700km",
        "origin": "M78星雲 光の国",
        "color_timer": "あり（残り3分で赤く点滅）",
        "type": None,
        "description": "ウルトラマン・セブンに続く3代目のウルトラ戦士。地球人・郷 秀樹と一体化して帰ってきた。ウルトラブレスレットという多機能武器を持ち、先輩ウルトラマンたちから技を受け継ぎながらも独自のスタイルで戦う。本作では兄弟・家族の絆をテーマとした深みある人間ドラマが描かれ、怪獣描写の迫力とともにシリーズを代表する傑作として評価が高い。",
        "image_url": None
    },
    {
        "name": "ウルトラマンエース",
        "alias": "北斗 星司（TAC 隊員）※第27話以降は単独変身",
        "series": "ウルトラマンA",
        "series_year": "1972年",
        "height": "65m",
        "weight": "55,000t",
        "age": "17,000歳",
        "flight_speed": "マッハ6",
        "run_speed": "時速800km",
        "origin": "M78星雲 光の国",
        "color_timer": "あり（残り3分で赤く点滅）",
        "type": None,
        "description": "超獣という新たな脅威に立ち向かうウルトラ戦士。当初は地球人の北斗 星司と南 夕子が合体するダブル変身を行っていたが、第27話以降は北斗 星司の単独変身に変更された。ウルトラ兄弟5番目の兄弟で、両腕をY字に組んで放つ「メタリウム光線」は圧倒的な威力を誇る。怪獣・宇宙人だけでなく人間の心の闇をも描いた重厚なストーリーが特徴。",
        "image_url": None
    },
    {
        "name": "ウルトラマンタロウ",
        "alias": "東 光太郎（ZAT 隊員）",
        "series": "ウルトラマンタロウ",
        "series_year": "1973年",
        "height": "53m",
        "weight": "55,000t",
        "age": "160,000歳",
        "flight_speed": "マッハ5",
        "run_speed": "時速900km",
        "origin": "M78星雲 光の国",
        "color_timer": "あり（残り3分で赤く点滅）",
        "type": None,
        "description": "ウルトラの父・母の実子であり、ウルトラ兄弟の末弟（6番目）。ウルトラ一族のサラブレッドとして最強クラスの戦闘力を誇り、ウルトラ兄弟全員のエネルギーを結集した「ストリウム光線」や全身を爆発させる「ウルトラダイナマイト」など豪快な必殺技が特徴。地球人・東 光太郎と一体化し、数々の強敵を打ち破った。",
        "image_url": None
    },
    {
        "name": "ゾフィー",
        "alias": "（変身者なし・宇宙警備隊 隊長）",
        "series": "ウルトラマン",
        "series_year": "1967年（初登場）",
        "height": "40m",
        "weight": "35,000t",
        "age": "25,000歳",
        "flight_speed": "マッハ7",
        "run_speed": "時速800km",
        "origin": "M78星雲 光の国",
        "color_timer": "なし",
        "type": None,
        "description": "M78星雲・宇宙警備隊の隊長を務めるウルトラ戦士で、ウルトラ兄弟の長兄。ウルトラマンの最終回「さらばウルトラマン」でバルタン星人に瀕死のダメージを負ったウルトラマンを迎えに来た姿が初登場。2つの命を持ち、その一つをハヤタに渡して地球に残させた。以降、多くのシリーズで登場し、ウルトラ一族の精神的支柱として後輩ウルトラマンたちを支えてきた。",
        "image_url": None
    },
]

# ================================================================
# 必殺技データ（ultraman_name でウルトラマンを紐づけ）
# ================================================================
moves_by_name = {
    "ウルトラマン": [
        {"name": "スペシウム光線",     "type": "光線技",  "order_no": 1, "description": "右腕の前に左腕を十字に当てて放つウルトラマン最強の必殺光線。膨大なウルトラエネルギーを凝縮した光の奔流で、ほとんどの怪獣を撃破してきたウルトラマンの代名詞的技。"},
        {"name": "八つ裂き光輪",       "type": "投擲技",  "order_no": 2, "description": "右腕を鎌状に曲げ、手首から発射する超高速の回転カッター。鋭い切れ味でゴモラの尻尾を切断したこともある。"},
        {"name": "ウルトラスラッシュ", "type": "投擲技",  "order_no": 3, "description": "腕から発する小型の円盤状カッター。八つ裂き光輪より小さく、素早い連続攻撃が可能。"},
        {"name": "電磁ネット",         "type": "捕縛技",  "order_no": 4, "description": "両手から放つ光のネット。怪獣を絡め取り動きを封じる。暴れる怪獣の拘束に使用。"},
        {"name": "ウルトラ水流",       "type": "特殊技",  "order_no": 5, "description": "口から放つ高圧の水流。炎を鎮めたり、熱性を持つ怪獣に対して有効。"},
        {"name": "テレキネシス",       "type": "念動力",  "order_no": 6, "description": "念力で物体を動かす超能力。重量物をも動かす強力な精神能力で、危機的状況での脱出にも活用される。"},
        {"name": "ウルトラバリヤー",   "type": "防御技",  "order_no": 7, "description": "全身を包む光のバリアを張る防御技。敵の攻撃を弾き返す。"},
    ],
    "ウルトラセブン": [
        {"name": "エメリウム光線",     "type": "光線技",  "order_no": 1, "description": "右目のビームランプから放つ必殺光線。スペシウム光線に匹敵する威力を誇り、多くの宇宙人・怪獣を倒してきたセブンの主力技。"},
        {"name": "アイスラッガー",     "type": "投擲技",  "order_no": 2, "description": "頭部のクレスト部分を外して投げる超高硬度のカッター。自在に操れる切断力とブーメランのように戻ってくる性能を持つセブンの代名詞的武器。"},
        {"name": "ワイドショット",     "type": "光線技",  "order_no": 3, "description": "両腕をL字に組んで放つ強力な放射状光線。広範囲の敵を一掃できる扇状の攻撃光線。"},
        {"name": "ハンドビーム",       "type": "光線技",  "order_no": 4, "description": "手のひらから放つ指向性の光線。比較的使用頻度が高く、素早い照射が可能。"},
        {"name": "セブンアロー",       "type": "投擲技",  "order_no": 5, "description": "弓矢の形をしたエネルギー体を投射する。貫通力が高く、遠距離の敵にも有効。"},
        {"name": "ウルトラノック戦法", "type": "格闘技",  "order_no": 6, "description": "格闘と光線を組み合わせた連続攻撃。相手の動きを封じながら確実にダメージを与えるセブンの格闘スタイル。"},
        {"name": "ビームランプ",       "type": "特殊技",  "order_no": 7, "description": "額のビームランプから放つ光線。エメリウム光線とは異なる形で放射することもでき、体力指標としても機能する。"},
    ],
    "ウルトラマンジャック": [
        {"name": "スペシウム光線",         "type": "光線技",  "order_no": 1, "description": "先輩ウルトラマンから受け継いだ必殺光線。両腕を十字に組んで放つ。初代と同様の動作で放つ由緒ある技。"},
        {"name": "ウルトラブレスレット",   "type": "投擲技",  "order_no": 2, "description": "腕輪型の多機能武器。ブーメランとして投擲したり、刃やメリケンサックに変形するなど状況に応じて様々な形態に変化。"},
        {"name": "ウルトラランス",         "type": "投擲技",  "order_no": 3, "description": "ウルトラブレスレットをエネルギーの槍状に変形させて投げる強力な投擲技。貫通力が高い。"},
        {"name": "ウルトラスラッシュ",     "type": "投擲技",  "order_no": 4, "description": "高速回転する円盤カッターを発射する投擲技。ウルトラブレスレットを応用した攻撃。"},
        {"name": "ウルトラシュート",       "type": "格闘技",  "order_no": 5, "description": "強烈なジャンプキックを繰り出す蹴り技。怪獣を大きく吹き飛ばす。"},
        {"name": "ブレスレットサンダー",   "type": "特殊技",  "order_no": 6, "description": "ウルトラブレスレットに電撃を纏わせた攻撃。電気系の強化技。"},
        {"name": "ウルトラアタック光線",   "type": "光線技",  "order_no": 7, "description": "強力なエネルギー光線。ウルトラ兄弟が教示した技を含め、多彩な光線技を習得している。"},
    ],
    "ウルトラマンエース": [
        {"name": "メタリウム光線",     "type": "光線技",  "order_no": 1, "description": "両腕をY字型に組んで放つ最強の必殺光線。圧倒的な威力を持ち、あらゆる超獣を撃破してきたエースの代名詞的技。"},
        {"name": "スペースQ",         "type": "空間技",  "order_no": 2, "description": "敵を異次元空間に閉じ込める技。超獣を完全に消滅させる特殊な能力。複数の敵に対しても効果を発揮する。"},
        {"name": "ウルトラギロチン",   "type": "切断技",  "order_no": 3, "description": "光のギロチンを生成し、怪獣の首を切断する技。一刀両断の切れ味を誇る。"},
        {"name": "マッハ回転アタック", "type": "格闘技",  "order_no": 4, "description": "高速回転しながら体当たりする格闘技。速度と体重を活かした強力な攻撃。"},
        {"name": "ランバルト光線",     "type": "光線技",  "order_no": 5, "description": "手のひらから放つ強力な光線。メタリウム光線とは異なる指向性を持つ。"},
        {"name": "バリヤー光線",       "type": "防御技",  "order_no": 6, "description": "光のバリアを張る防御技。敵の攻撃を跳ね返すとともに反撃にも転用できる。"},
        {"name": "アンチ光線",         "type": "光線技",  "order_no": 7, "description": "特定の超獣の能力を無効化するために放つ指向性光線。弱点を突く戦略的な技。"},
    ],
    "ウルトラマンタロウ": [
        {"name": "ストリウム光線",       "type": "光線技",  "order_no": 1, "description": "胸のストリウム球から放つタロウの最強光線。ウルトラ兄弟6人のエネルギーを結集した究極の必殺技で、威力は歴代最高クラス。"},
        {"name": "ウルトラダイナマイト", "type": "爆発技",  "order_no": 2, "description": "全身を炎に包んで敵に体当たりし、大爆発を起こす捨て身の必殺技。使用後は体がバラバラになるが再生する。"},
        {"name": "ウルトラランス",       "type": "投擲技",  "order_no": 3, "description": "エネルギーを槍状に変えて投げる強力な投擲技。ジャックから受け継いだ技で、貫通力が高い。"},
        {"name": "コスモミラクル光線",   "type": "光線技",  "order_no": 4, "description": "ウルトラ兄弟全員のエネルギーを結集した最終奥義。タロウが追い詰められた際に発動する圧倒的光線。"},
        {"name": "ウルトラアロー",       "type": "投擲技",  "order_no": 5, "description": "エネルギーを矢状に変形させて発射する投擲技。命中精度が高く、遠距離の敵にも有効。"},
        {"name": "タロウキック",         "type": "格闘技",  "order_no": 6, "description": "力強いジャンプキック。ウルトラ一族最高クラスの脚力から繰り出される強烈な蹴り技。"},
        {"name": "ウルトラ念力",         "type": "念動力",  "order_no": 7, "description": "念力で物体を操る能力。重量のある物体を遠隔操作でき、戦闘補助にも活用される。"},
    ],
    "ゾフィー": [
        {"name": "M87光線",             "type": "光線技",  "order_no": 1, "description": "両腕を斜めに交差させて放つ必殺光線。ウルトラ兄弟の中でも最高クラスの威力を誇り、隊長の名に恥じない圧倒的な攻撃力を持つ。"},
        {"name": "生命エネルギー注入",   "type": "蘇生技",  "order_no": 2, "description": "自身の命のエネルギーを注入して他者を蘇生させる技。ウルトラマン最終回でハヤタを蘇生させるために使用した、ゾフィーの慈悲を象徴する技。"},
        {"name": "ゾフィービーム",       "type": "光線技",  "order_no": 3, "description": "両手から放つ強力なエネルギービーム。素早い照射が可能で、近距離・遠距離を問わず使用できる。"},
        {"name": "スペースQ",           "type": "空間技",  "order_no": 4, "description": "敵を異次元空間に封じ込める技。エースとも共通する技で、宇宙警備隊の標準技術のひとつ。"},
        {"name": "ウルトラダブルアロー", "type": "合体技",  "order_no": 5, "description": "ウルトラマンジャックとの合体必殺技。2人のエネルギーを結集させた強力な投擲攻撃。"},
        {"name": "ウルトラ念力",         "type": "念動力",  "order_no": 6, "description": "念力で物体や敵を操る高度な精神能力。長い経験から培われた練度の高い念動力技術。"},
        {"name": "ウルトラバリヤー",     "type": "防御技",  "order_no": 7, "description": "光のバリアで攻撃を防ぐ防御技。隊長として仲間や地球を守るために使用する。"},
    ],
}

# ================================================================
# Supabase へのデータ投入
# ================================================================
def post_json(endpoint, rows, prefer="return=minimal"):
    data = json.dumps(rows).encode("utf-8")
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/{endpoint}",
        data=data,
        headers={
            "apikey": SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
            "Content-Type": "application/json",
            "Prefer": prefer
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as res:
        body = res.read().decode("utf-8")
        return res.status, json.loads(body) if body else []

# Step 1: ultraman テーブルへ投入（ID を取得するため representation で返す）
print("▶ ウルトラマン基本情報を投入中...")
try:
    status, inserted = post_json("ultraman", ultraman_rows, prefer="return=representation")
    print(f"  成功: HTTP {status}, {len(inserted)}件")
except urllib.error.HTTPError as e:
    print(f"  エラー: HTTP {e.code}")
    print(e.read().decode("utf-8"))
    exit(1)

# name → id のマッピングを作成
id_map = {r["name"]: r["id"] for r in inserted}
print(f"  IDマップ: {id_map}")

# Step 2: ultraman_moves テーブルへ投入
print("\n▶ 必殺技データを投入中...")
all_moves = []
for um_name, moves in moves_by_name.items():
    um_id = id_map.get(um_name)
    if um_id is None:
        print(f"  警告: '{um_name}' のIDが見つかりません")
        continue
    for move in moves:
        all_moves.append({
            "ultraman_id": um_id,
            "name": move["name"],
            "type": move["type"],
            "description": move["description"],
            "order_no": move["order_no"]
        })

try:
    status, _ = post_json("ultraman_moves", all_moves)
    print(f"  成功: HTTP {status}, {len(all_moves)}件")
except urllib.error.HTTPError as e:
    print(f"  エラー: HTTP {e.code}")
    print(e.read().decode("utf-8"))
    exit(1)

print("\n✅ 全データの投入が完了しました")
print(f"   ウルトラマン: {len(ultraman_rows)}件")
print(f"   必殺技: {len(all_moves)}件")
