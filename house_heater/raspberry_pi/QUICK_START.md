# ⚡ 빠른 시작 가이드

라즈베리파이에서 5분 안에 실행하기!

## 🎯 전제 조건

- ✅ 라즈베리파이 OS 설치 완료
- ✅ SSH 접속 가능 (또는 직접 접속)
- ✅ 인터넷 연결
- ✅ Supabase 프로젝트 생성 완료
- ✅ `supabase_setup.sql` 실행 완료

---

## 📝 1단계: 파일 준비

### 옵션 A: Git 사용 (권장)

```bash
cd ~
git clone YOUR_REPOSITORY_URL house_heater
cd house_heater/raspberry_pi
```

### 옵션 B: 직접 파일 업로드

1. PC에서 `raspberry_pi` 폴더를 압축
2. SCP 또는 USB로 라즈베리파이에 전송
3. 압축 해제 후 해당 디렉토리로 이동

---

## 📝 2단계: 자동 설치

```bash
# 실행 권한 부여
chmod +x install.sh

# 설치 스크립트 실행
./install.sh
```

이 스크립트는 다음을 자동으로 수행합니다:
- ✅ 시스템 패키지 설치 (pigpio, python3-pip)
- ✅ Python 패키지 설치
- ✅ 파일 복사 및 권한 설정

---

## 📝 3단계: Supabase 정보 입력

### Supabase 정보 확인

1. Supabase 대시보드 접속
2. Settings > API 메뉴
3. 다음 정보 복사:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJhbGc...` (긴 문자열)

### 서비스 파일 편집

```bash
sudo nano ~/boiler_controller/boiler-controller.service
```

다음 두 줄을 찾아서 실제 값으로 변경:

```ini
Environment="SUPABASE_URL=https://xxxxx.supabase.co"    # ← 실제 URL
Environment="SUPABASE_KEY=eyJhbGc..."                    # ← 실제 KEY
```

**저장:** `Ctrl + O`, `Enter`, `Ctrl + X`

---

## 📝 4단계: 서비스 시작

```bash
# 서비스 파일 복사
sudo cp ~/boiler_controller/boiler-controller.service /etc/systemd/system/

# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable boiler-controller.service
sudo systemctl start boiler-controller.service
```

---

## 📝 5단계: 확인

```bash
# 서비스 상태 확인 (초록색 "active (running)" 표시 확인)
sudo systemctl status boiler-controller.service

# 로그 확인 (오류 메시지 없는지 확인)
sudo journalctl -u boiler-controller.service -n 50
```

**정상 작동 시 로그 예시:**
```
INFO - Supabase 클라이언트 초기화 완료
INFO - 서보모터 초기화 완료 (GPIO 18)
INFO - 초기 모드: mode_0
INFO - Realtime 구독 성공. 대기 중...
```

---

## 🎉 완료!

이제 웹 UI에서 보일러 모드를 변경하면 라즈베리파이가 자동으로 반응합니다!

---

## 🔧 문제가 생겼다면?

### 서비스가 시작되지 않음

```bash
# 오류 확인
sudo journalctl -u boiler-controller.service -n 100

# 주요 확인 사항:
# 1. Supabase URL/KEY가 올바른지
# 2. pigpio 데몬이 실행 중인지: sudo systemctl status pigpiod
# 3. Python 패키지가 설치되었는지: pip3 list | grep supabase
```

### 수동 실행으로 테스트

```bash
cd ~/boiler_controller
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key-here"
python3 boiler_controller.py
```

오류 메시지를 확인하고 수정하세요.

---

## 📚 더 자세한 설명이 필요하면?

`INSTALL_GUIDE.md` 파일을 참조하세요!

