-- ============================================
-- 스마트 난방 조절기 프로젝트 - Supabase 설정
-- ============================================

-- 제어 테이블 생성
CREATE TABLE IF NOT EXISTS boiler_control (
    id INT PRIMARY KEY DEFAULT 1,
    mode TEXT NOT NULL, -- 'mode_0' (실내난방), 'mode_60' (온수전용)
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 초기값 설정 (테이블이 비어있을 경우에만)
INSERT INTO boiler_control (id, mode) 
VALUES (1, 'mode_0')
ON CONFLICT (id) DO NOTHING;

-- Realtime 활성화 (변경 사항을 실시간으로 구독할 수 있도록)
ALTER PUBLICATION supabase_realtime ADD TABLE boiler_control;

-- 로그 테이블 (선택사항 - 동작 기록 저장)
CREATE TABLE IF NOT EXISTS boiler_logs (
    id BIGSERIAL PRIMARY KEY,
    mode TEXT NOT NULL,
    action_time TIMESTAMPTZ DEFAULT NOW(),
    source TEXT -- 'user', 'schedule', 'auto' 등
);

-- 인덱스 추가 (로그 조회 성능 향상)
CREATE INDEX IF NOT EXISTS idx_boiler_logs_action_time ON boiler_logs(action_time DESC);

