import json, urllib.request

SUPABASE_URL = "https://cbxipgqfhbsmgmatherr.supabase.co"
# service_role キーを使用（Supabase ダッシュボード → Settings → API → service_role）
# このキーはここにのみ記載し、HTML には絶対に書かないこと
SERVICE_ROLE_KEY = "ここにservice_roleキーを貼り付ける"

rows = [
    {
        "name": "アーナガルゲ",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "中央アルプス・阿賀鉱山",
        "height": "64m",
        "weight": "8万t",
        "desc": "中央アルプスの阿賀鉱山に棲息していた鉱脈怪獣。ダークマターの影響を受けて地底から出現し、鉱山周辺を破壊した。ネオスの活躍により倒された。",
        "episode": "第1話",
        "episode_name": "ネオス誕生",
        "tc": "g",
        "tags": "鉱脈怪獣"
    },
    {
        "name": "ザム星人",
        "series": "ウルトラマンネオス",
        "type": "星人",
        "origin": "YY星系第9惑星ザム星",
        "height": "60m",
        "weight": "6万5千t",
        "desc": "YY星系第9惑星ザム星からやってきた脳魂宇宙人。地球侵略を目論む知性的な宇宙人であり、ダークマターを利用して怪獣を操る。作中で複数体が登場した。",
        "episode": "第2話",
        "episode_name": "謎のダークマター",
        "tc": "r",
        "tags": "脳魂宇宙人"
    },
    {
        "name": "シーゴリアン",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "長井港近海",
        "height": "69m",
        "weight": "5万2千t",
        "desc": "長井港近海の深海に棲息していた群体怪獣。無数の個体が合体することで巨大な一体の怪獣となる。海から上陸して港湾施設に甚大な被害をもたらした。",
        "episode": "第3話",
        "episode_name": "海からのSOS",
        "tc": "blue",
        "tags": "群体怪獣"
    },
    {
        "name": "ノゼラ",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "北極",
        "height": "65m",
        "weight": "7万3千t",
        "desc": "北極に棲息していた北極怪獣。ダークマターの影響を受けて活性化し、凍てつく冷気を武器として戦う。セブン21と交戦した強敵の一体。",
        "episode": "第4話",
        "episode_name": "赤い巨人! セブン21",
        "tc": "blue",
        "tags": "北極怪獣"
    },
    {
        "name": "サゾラ",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "南極",
        "height": "70m",
        "weight": "3万6千t",
        "desc": "南極に棲息していた南極怪獣。ノゼラとともにダークマターの影響を受けて出現し、セブン21およびネオスと戦った。巨大な体躯を持ち、強力な攻撃力を誇る。",
        "episode": "第4話",
        "episode_name": "赤い巨人! セブン21",
        "tc": "blue",
        "tags": "南極怪獣"
    },
    {
        "name": "シルドバン",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "あさひが丘団地付近",
        "height": "50m",
        "weight": "4万9千t",
        "desc": "あさひが丘団地付近に出現した昆虫怪獣。ダークマターの影響で巨大化・凶暴化した昆虫系の怪獣で、バッカクーンと関連する。鋭い脚と外殻が武器。",
        "episode": "第5話",
        "episode_name": "見えない絆",
        "tc": "g",
        "tags": "昆虫怪獣"
    },
    {
        "name": "バッカクーン",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "あさひが丘造成地",
        "height": "49m",
        "weight": "4万7千t",
        "desc": "あさひが丘造成地に出現した寄生怪獣。他の生物に寄生してその宿主を操る能力を持ち、シルドバンとともに第5話に登場した。寄生により宿主を急成長させる。",
        "episode": "第5話",
        "episode_name": "見えない絆",
        "tc": "g",
        "tags": "寄生怪獣"
    },
    {
        "name": "ザムリベンジャー",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "宇宙",
        "height": "63m",
        "weight": "7万2千t",
        "desc": "ザム星人の残党がネオスへの復讐のために送り込んだ巨大な復讐ロボット。高い戦闘力と耐久性を持ち、ネオスを苦しめた。機械の体に強力な武装を備える。",
        "episode": "第6話",
        "episode_name": "ザム星人の復讐",
        "tc": "r",
        "tags": "復讐ロボット"
    },
    {
        "name": "ロックイーター",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "荒神島",
        "height": "64m",
        "weight": "7万t",
        "desc": "荒神島に棲息していた凶暴竜。島の生態系の頂点に君臨していた大型怪獣で、強靭な顎と爪を武器とする。キングバモスとともに第7話に登場した。",
        "episode": "第7話",
        "episode_name": "生態系の王",
        "tc": "g",
        "tags": "凶暴竜"
    },
    {
        "name": "キングバモス",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "荒神島",
        "height": "62m",
        "weight": "6万5千t",
        "desc": "荒神島に棲息していた変貌怪獣。ダークマターの影響を受けて次々と変身・進化する能力を持つ怪獣。ロックイーターとともに荒神島の生態系を支配していた。",
        "episode": "第7話",
        "episode_name": "生態系の王",
        "tc": "g",
        "tags": "変貌怪獣"
    },
    {
        "name": "ラフレシオン",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "宮崎沖海中",
        "height": "66m",
        "weight": "7万4千t",
        "desc": "宮崎沖の深海に棲息していた幻聖魔獣。妖艶な光と幻惑能力を持ち、大型の花のような外見を持つ怪獣。海から出現してHEARTの隊員たちを苦しめた。",
        "episode": "第8話",
        "episode_name": "蘇る地球 HEART南へ!",
        "tc": "g",
        "tags": "幻聖魔獣"
    },
    {
        "name": "キングダイナス",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "グリーンランド裏山",
        "height": "67m",
        "weight": "7万8千t",
        "desc": "グリーンランドの山中に出現した合体恐竜。複数の恐竜系怪獣が合体して誕生した巨大怪獣で、強力なパワーを誇る。子どもたちのいるコースター付近で戦闘となった。",
        "episode": "第9話",
        "episode_name": "僕らの恐竜コースター",
        "tc": "g",
        "tags": "合体恐竜"
    },
    {
        "name": "ギガドレッド",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "成層圏",
        "height": "62m",
        "weight": "8万5千t",
        "desc": "成層圏から飛来した隕石怪獣。宇宙空間を漂いながら隕石とともにやってきた怪獣で、HEARTのSXが遭遇した。強固な岩石質の外皮と破壊エネルギーを持つ。",
        "episode": "第10話",
        "episode_name": "決断せよ! SX救出作戦",
        "tc": "r",
        "tags": "隕石怪獣"
    },
    {
        "name": "グラール",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "宇宙",
        "height": "66m",
        "weight": "6万6千t",
        "desc": "メンシュハイトが各怪獣の特性を合成して作り上げた究極の暗殺怪獣。黄金に輝く体と二対の赤い眼を持ち、火炎弾や拡散破壊光線など多彩な能力を誇る最強の刺客。",
        "episode": "第11話",
        "episode_name": "宇宙からの暗殺獣",
        "tc": "r",
        "tags": "暗殺怪獣"
    },
    {
        "name": "メンシュハイト",
        "series": "ウルトラマンネオス",
        "type": "怪獣",
        "origin": "宇宙",
        "height": "69m",
        "weight": "9万6千t",
        "desc": "宇宙から地球に迫る究極進化帝王。ダークマターを操る能力を持ち、地球侵略の黒幕として君臨する最強の敵。第11・12話に登場し、ネオスと最終決戦を繰り広げた。",
        "episode": "第11話・第12話",
        "episode_name": "宇宙からの暗殺獣 / 光の戦士よ永遠に",
        "tc": "r",
        "tags": "究極進化帝王"
    }
]

data = json.dumps(rows).encode("utf-8")
req = urllib.request.Request(
    f"{SUPABASE_URL}/rest/v1/kaiju",
    data=data,
    headers={
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    },
    method="POST"
)
try:
    with urllib.request.urlopen(req) as res:
        print(f"追加成功: HTTP {res.status}")
        print(f"追加件数: {len(rows)}件")
except urllib.error.HTTPError as e:
    print(f"エラー: HTTP {e.code}")
    print(e.read().decode("utf-8"))
