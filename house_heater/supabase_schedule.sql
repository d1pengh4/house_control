-- ============================================
-- 시간 예약 자동화 (pg_cron)
-- ============================================
-- 
-- 주의: pg_cron은 Supabase에서 직접 사용할 수 없습니다.
-- 대신 Supabase Edge Functions 또는 외부 cron 서비스(예: GitHub Actions, Vercel Cron)를 사용해야 합니다.
--
-- 아래는 pg_cron이 사용 가능한 환경(자체 PostgreSQL 서버)을 위한 예제입니다.
-- Supabase에서는 Supabase Edge Functions 또는 외부 서비스를 권장합니다.
--

-- ============================================
-- 방법 1: pg_cron 사용 (자체 PostgreSQL 서버)
-- ============================================

-- 확장 기능 활성화
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- 매일 오전 7시에 실내 난방 모드(0도)로 전환
SELECT cron.schedule(
    'morning-heating-mode',
    '0 7 * * *',  -- 매일 7시 0분
    $$
    UPDATE boiler_control 
    SET mode = 'mode_0', updated_at = NOW() 
    WHERE id = 1;
    
    INSERT INTO boiler_logs (mode, source) 
    VALUES ('mode_0', 'schedule_morning');
    $$
);

-- 매일 밤 11시에 온수 전용 모드(60도)로 전환
SELECT cron.schedule(
    'night-hotwater-mode',
    '0 23 * * *',  -- 매일 23시 0분
    $$
    UPDATE boiler_control 
    SET mode = 'mode_60', updated_at = NOW() 
    WHERE id = 1;
    
    INSERT INTO boiler_logs (mode, source) 
    VALUES ('mode_60', 'schedule_night');
    $$
);

-- 스케줄 확인
SELECT * FROM cron.job;

-- 스케줄 삭제 (필요시)
-- SELECT cron.unschedule('morning-heating-mode');
-- SELECT cron.unschedule('night-hotwater-mode');

-- ============================================
-- 방법 2: Supabase Edge Function 사용 권장
-- ============================================
--
-- Supabase에서는 pg_cron 대신 Edge Functions와 
-- 외부 cron 서비스(GitHub Actions, Vercel Cron 등)를 사용하는 것이 좋습니다.
--
-- 1. Supabase Edge Function 생성:
--    - boiler-schedule 함수 생성
--    - mode 파라미터를 받아서 boiler_control 업데이트
--
-- 2. GitHub Actions 또는 Vercel Cron에서:
--    - 매일 7시에 Edge Function 호출 (mode_0)
--    - 매일 23시에 Edge Function 호출 (mode_60)
--
-- 예시 GitHub Actions workflow:
--
-- name: Boiler Schedule
-- on:
--   schedule:
--     - cron: '0 7 * * *'  # 오전 7시
--     - cron: '0 23 * * *' # 밤 11시
-- jobs:
--   update-boiler:
--     runs-on: ubuntu-latest
--     steps:
--       - name: Set mode for 7am
--         if: github.event.schedule == '0 7 * * *'
--         run: |
--           curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/boiler-schedule \
--             -H "Authorization: Bearer YOUR_ANON_KEY" \
--             -H "Content-Type: application/json" \
--             -d '{"mode": "mode_0"}'
--       - name: Set mode for 11pm
--         if: github.event.schedule == '0 23 * * *'
--         run: |
--           curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/boiler-schedule \
--             -H "Authorization: Bearer YOUR_ANON_KEY" \
--             -H "Content-Type: application/json" \
--             -d '{"mode": "mode_60"}'

