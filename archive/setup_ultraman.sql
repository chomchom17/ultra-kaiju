-- ================================================================
-- ウルトラマンテーブル作成スクリプト
-- Supabase の SQL Editor で実行してください
-- ================================================================

-- ウルトラマン基本情報テーブル
CREATE TABLE IF NOT EXISTS ultraman (
  id           SERIAL PRIMARY KEY,
  name         TEXT NOT NULL,          -- ウルトラマン名
  alias        TEXT,                   -- 変身者（例: ハヤタ・シン）
  series       TEXT,                   -- 主要出演シリーズ名
  series_year  TEXT,                   -- 放映年
  height       TEXT,                   -- 身長
  weight       TEXT,                   -- 体重
  age          TEXT,                   -- 年齢
  flight_speed TEXT,                   -- 飛行速度
  run_speed    TEXT,                   -- 走行速度
  origin       TEXT,                   -- 出身地
  color_timer  TEXT,                   -- カラータイマー情報
  type         TEXT,                   -- タイプ・形態
  description  TEXT,                   -- 詳細説明
  image_url    TEXT,                   -- 画像URL（将来用）
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- 必殺技テーブル
CREATE TABLE IF NOT EXISTS ultraman_moves (
  id           SERIAL PRIMARY KEY,
  ultraman_id  INTEGER NOT NULL REFERENCES ultraman(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,          -- 技名
  type         TEXT,                   -- 技種別（光線技・投擲技・格闘技 など）
  description  TEXT,                   -- 技の説明
  order_no     INTEGER DEFAULT 0       -- 表示順
);

-- ================================================================
-- Row Level Security の設定
-- ================================================================
ALTER TABLE ultraman ENABLE ROW LEVEL SECURITY;
ALTER TABLE ultraman_moves ENABLE ROW LEVEL SECURITY;

-- 読み取り：全公開
CREATE POLICY "allow_select" ON ultraman
  FOR SELECT USING (true);

CREATE POLICY "allow_select" ON ultraman_moves
  FOR SELECT USING (true);

-- 書き込み：anonキーからのINSERT許可（upload スクリプト用）
CREATE POLICY "allow_insert" ON ultraman
  FOR INSERT WITH CHECK (true);

CREATE POLICY "allow_insert" ON ultraman_moves
  FOR INSERT WITH CHECK (true);
