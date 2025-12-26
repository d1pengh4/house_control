# 🚀 다음 단계 실행 가이드

프로젝트를 실제로 실행하기 위한 단계별 가이드입니다.

---

## 📋 체크리스트

- [x] 코드 작성 완료
- [x] Supabase URL/KEY 설정 완료
- [ ] Supabase 데이터베이스 초기화
- [ ] 라즈베리파이 설치 및 실행
- [ ] 웹 UI 배포
- [ ] 테스트 및 확인

---

## 1️⃣ Supabase 데이터베이스 초기화 (5분)

### 단계 1: Supabase 대시보드 접속

1. https://supabase.com 접속
2. 프로젝트 선택: `ajtjxkngstbzbjhvtkdr`
3. 왼쪽 메뉴에서 **SQL Editor** 클릭

### 단계 2: SQL 스크립트 실행

1. **New Query** 클릭
2. `supabase_setup.sql` 파일의 모든 내용을 복사해서 붙여넣기
3. **Run** 버튼 클릭 (또는 `Cmd/Ctrl + Enter`)

**실행할 SQL 내용:**
```sql
-- 제어 테이블 생성
CREATE TABLE IF NOT EXISTS boiler_control (
    id INT PRIMARY KEY DEFAULT 1,
    mode TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 초기값 설정
INSERT INTO boiler_control (id, mode) 
VALUES (1, 'mode_0')
ON CONFLICT (id) DO NOTHING;

-- Realtime 활성화
ALTER PUBLICATION supabase_realtime ADD TABLE boiler_control;

-- 로그 테이블 생성 (선택사항)
CREATE TABLE IF NOT EXISTS boiler_logs (
    id BIGSERIAL PRIMARY KEY,
    mode TEXT NOT NULL,
    action_time TIMESTAMPTZ DEFAULT NOW(),
    source TEXT
);

-- 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_boiler_logs_action_time ON boiler_logs(action_time DESC);
```

### 단계 3: Realtime 활성화 확인

1. 왼쪽 메뉴에서 **Database** > **Replication** 클릭
2. `boiler_control` 테이블이 목록에 있고 활성화되어 있는지 확인

### 단계 4: 테이블 확인

1. 왼쪽 메뉴에서 **Table Editor** 클릭
2. `boiler_control` 테이블이 생성되었는지 확인
3. 초기 데이터가 `mode: mode_0`로 설정되어 있는지 확인

**✅ 완료 기준:** 
- SQL 실행 성공 메시지 확인
- `boiler_control` 테이블에 데이터가 있음

---

## 2️⃣ 라즈베리파이 설치 및 실행 (15-20분)

### 전제 조건 확인

- [ ] 라즈베리파이 제로 2W (또는 다른 모델)
- [ ] 라즈베리파이 OS 설치 완료
- [ ] 인터넷 연결 (Wi-Fi 또는 이더넷)
- [ ] SSH 접속 가능 (또는 직접 접속)

### 방법 A: 빠른 설치 (자동 스크립트)

#### 1단계: 파일 전송

**옵션 1: Git 사용 (권장)**
```bash
# 라즈베리파이에서
cd ~
git clone YOUR_REPOSITORY_URL house_heater
cd house_heater/raspberry_pi
```

**옵션 2: SCP 사용**
```bash
# PC/Mac에서 (터미널)
scp -r raspberry_pi pi@라즈베리파이_IP주소:~/boiler_controller
```

**옵션 3: USB 또는 직접 복사**
- MicroSD 카드 또는 USB로 파일 복사

#### 2단계: 자동 설치 스크립트 실행

```bash
# 라즈베리파이에서
cd ~/boiler_controller  # 또는 파일이 있는 위치
chmod +x install.sh
./install.sh
```

이 스크립트가 자동으로:
- ✅ 시스템 패키지 설치 (pigpio, python3-pip)
- ✅ Python 패키지 설치
- ✅ 파일 복사 및 권한 설정

#### 3단계: 서비스 시작

```bash
# 서비스 파일 복사 (이미 Supabase 정보가 설정되어 있음)
sudo cp boiler-controller.service /etc/systemd/system/

# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable boiler-controller.service
sudo systemctl start boiler-controller.service

# 상태 확인 (초록색 "active (running)" 확인)
sudo systemctl status boiler-controller.service
```

#### 4단계: 로그 확인

```bash
# 실시간 로그 확인
sudo journalctl -u boiler-controller.service -f

# 최근 로그 50줄 확인
sudo journalctl -u boiler-controller.service -n 50
```

**정상 작동 시 로그 예시:**
```
INFO - Supabase 클라이언트 초기화 완료
INFO - 서보모터 초기화 완료 (GPIO 18)
INFO - 초기 모드: mode_0
INFO - Realtime 구독 성공. 대기 중...
```

**✅ 완료 기준:**
- 서비스 상태가 `active (running)`
- 로그에 오류 메시지 없음
- "Realtime 구독 성공" 메시지 확인

---

## 3️⃣ 웹 UI 배포 (5-10분)

웹 UI를 배포하는 여러 방법이 있습니다. 가장 쉬운 방법부터 설명합니다.

### 방법 1: GitHub Pages (가장 쉬움, 무료)

#### 1단계: GitHub 저장소 생성

1. https://github.com 접속
2. **New repository** 클릭
3. 저장소 이름 입력 (예: `house-heater-web`)
4. **Public** 또는 **Private** 선택
5. **Create repository** 클릭

#### 2단계: 파일 업로드

1. 저장소 페이지에서 **uploading an existing file** 클릭
2. `web/index.html` 파일 드래그 앤 드롭
3. **Commit changes** 클릭

#### 3단계: GitHub Pages 활성화

1. 저장소 페이지에서 **Settings** 클릭
2. 왼쪽 메뉴에서 **Pages** 클릭
3. **Source**에서 **Deploy from a branch** 선택
4. Branch를 `main` (또는 `master`) 선택
5. **Save** 클릭
6. 몇 분 후 페이지 URL 확인 (예: `https://username.github.io/house-heater-web/`)

**⚠️ 보안 주의:** 
- Public 저장소에 실제 키를 올리면 누구나 볼 수 있습니다.
- Private 저장소를 사용하거나, 다른 배포 방법을 고려하세요.

### 방법 2: Netlify Drop (빠름, 무료, 키 보호)

1. https://app.netlify.com/drop 접속
2. `web/index.html` 파일을 드래그 앤 드롭
3. 자동으로 배포된 URL 확인
4. 키는 여전히 코드에 노출되므로 주의 필요

### 방법 3: 로컬 웹 서버 (개인 사용)

```bash
# 라즈베리파이 또는 PC에서
cd web
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000` 또는 `http://라즈베리파이_IP:8000` 접속

### 방법 4: 라즈베리파이에 직접 호스팅

```bash
# 라즈베리파이에서
cd ~
sudo apt install nginx
sudo cp ~/house_heater/web/index.html /var/www/html/
```

브라우저에서 `http://라즈베리파이_IP주소` 접속

**✅ 완료 기준:**
- 웹 페이지가 정상적으로 로드됨
- PIN 입력 화면이 나타남

---

## 4️⃣ 하드웨어 연결 (10분)

### 서보모터 연결

| 서보모터 핀 | 라즈베리파이 핀 | 물리 핀 번호 |
|------------|---------------|------------|
| 빨간색 (VCC) | 5V | 2번 |
| 갈색/검은색 (GND) | GND | 6번 |
| 주황색 (Signal) | GPIO 18 | 12번 |

**연결 순서:**
1. 라즈베리파이 전원 차단
2. 위 표에 따라 와이어 연결
3. 서보모터 본체를 글루건으로 고정 (떨림 방지)
4. 라즈베리파이 전원 켜기

### 각도 조정 (필수)

보일러 스위치의 실제 위치에 맞게 각도 조정:

```bash
# 라즈베리파이에서
nano ~/boiler_controller/boiler_controller.py
```

다음 부분 찾기:
```python
ANGLE_0 = -1.0    # 0도 위치
ANGLE_60 = 0.33   # 60도 위치
```

각도를 조금씩 변경하면서 테스트하세요.

**✅ 완료 기준:**
- 서보모터가 0도와 60도 위치에서 정확히 회전
- 보일러 스위치와 정확히 연결됨

---

## 5️⃣ 테스트 및 확인 (10분)

### 테스트 1: 웹 UI 접속

1. 스마트폰 또는 PC 브라우저에서 웹 UI URL 접속
2. PIN 번호 입력 (`1234`)
3. 메인 화면이 나타나는지 확인

### 테스트 2: 모드 변경

1. 웹 UI에서 "🔥 실내 난방 (0도)" 버튼 클릭
2. 화면에 "처리 중..." 표시 확인
3. 현재 모드가 업데이트되는지 확인
4. 라즈베리파이 로그 확인:

```bash
sudo journalctl -u boiler-controller.service -f
```

예상 로그:
```
INFO - 모드 변경: None -> mode_0
INFO - 서보모터 이동 중: -1.0
INFO - 서보모터 이동 완료: -1.0
```

5. 서보모터가 실제로 회전하는지 확인

### 테스트 3: 반대 모드로 변경

1. "💧 온수 전용 (60도)" 버튼 클릭
2. 서보모터가 60도 위치로 회전하는지 확인

### 테스트 4: Supabase 확인

1. Supabase 대시보드 > Table Editor > `boiler_control` 클릭
2. `mode` 값이 변경되었는지 확인
3. `updated_at` 타임스탬프가 업데이트되었는지 확인

**✅ 완료 기준:**
- 웹 UI에서 버튼 클릭 시 정상 동작
- 라즈베리파이 로그에 정상 메시지
- 서보모터가 정확히 회전
- Supabase DB 값이 변경됨

---

## 🐛 문제 해결

### 웹 UI에서 "모드 변경 실패"

1. Supabase 연결 확인:
   - 브라우저 개발자 도구 (F12) > Console 탭에서 오류 확인
   - Supabase URL/KEY가 올바른지 확인

2. Supabase 테이블 확인:
   - Table Editor에서 `boiler_control` 테이블 확인
   - 데이터가 있는지 확인

### 라즈베리파이에서 "Realtime 구독 실패"

```bash
# 로그 확인
sudo journalctl -u boiler-controller.service -n 100

# 환경 변수 확인
sudo systemctl show boiler-controller.service | grep Environment

# 수동 실행으로 테스트
cd ~/boiler_controller
export SUPABASE_URL="https://ajtjxkngstbzbjhvtkdr.supabase.co"
export SUPABASE_KEY="sb_publishable_CEWJ_yVJQQOGHpAK43dhJQ_X0bIkX6h"
python3 boiler_controller.py
```

### 서보모터가 작동하지 않음

1. pigpio 데몬 확인:
```bash
sudo systemctl status pigpiod
sudo systemctl restart pigpiod
```

2. GPIO 연결 확인:
   - 핀 연결이 올바른지 확인
   - 서보모터 전원 확인

3. 권한 확인:
```bash
sudo usermod -a -G gpio pi
```

---

## 📚 추가 참고 자료

- **상세 설치 가이드**: `raspberry_pi/INSTALL_GUIDE.md`
- **빠른 시작**: `raspberry_pi/QUICK_START.md`
- **유저 플로우**: `USER_FLOW.md`
- **전체 README**: `README.md`

---

## 🎉 완료!

모든 단계가 완료되면 다음과 같이 사용할 수 있습니다:

1. **스마트폰에서 웹 UI 접속**
2. **PIN 번호 입력**
3. **버튼 클릭으로 보일러 모드 변경**
4. **약 0.8초 내에 보일러 스위치가 자동으로 회전**

행운을 빕니다! 문제가 발생하면 로그를 확인하고 위의 문제 해결 섹션을 참고하세요.

