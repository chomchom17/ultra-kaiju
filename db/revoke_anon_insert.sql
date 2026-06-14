-- ================================================================
-- anon ロールの INSERT 権限を削除する
-- Supabase SQL Editor で実行してください
--
-- 実行後は upload スクリプトの実行に service_role キーが必要になります。
-- service_role キーは Supabase ダッシュボード →
--   Settings → API → "service_role" の欄から取得できます。
-- ================================================================

-- kaiju テーブル（既存）
DROP POLICY IF EXISTS "allow_insert" ON kaiju;
DROP POLICY IF EXISTS "Allow anon insert" ON kaiju;

-- ultraman テーブル（新規）
DROP POLICY IF EXISTS "allow_insert" ON ultraman;
DROP POLICY IF EXISTS "Allow anon insert" ON ultraman;

-- ultraman_moves テーブル（新規）
DROP POLICY IF EXISTS "allow_insert" ON ultraman_moves;
DROP POLICY IF EXISTS "Allow anon insert" ON ultraman_moves;

-- ================================================================
-- 確認: SELECT のみ残っていることを確認
-- ================================================================
SELECT schemaname, tablename, policyname, cmd
FROM pg_policies
WHERE tablename IN ('kaiju', 'ultraman', 'ultraman_moves')
ORDER BY tablename, cmd;
