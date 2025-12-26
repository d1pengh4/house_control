# 🔥 스마트 난방 조절기 프로젝트

라즈베리파이 제로 2W와 Supabase 클라우드를 연동하여 보일러 스위치를 원격 제어하는 시스템입니다.

## 📋 목차

- [시스템 개요](#시스템-개요)
- [구성 요소](#구성-요소)
- [설치 가이드](#설치-가이드)
- [사용 방법](#사용-방법)
- [하드웨어 연결](#하드웨어-연결)
- [문제 해결](#문제-해결)

## 🎯 시스템 개요

이 프로젝트는 다음 기능을 제공합니다:

- **원격 제어**: 스마트폰 웹 UI를 통해 보일러 모드를 원격으로 변경
- **실시간 동기화**: Supabase Realtime을 통해 즉시 상태 반영 (0.1초 내)
- **자동 예약**: 특정 시간에 자동으로 모드 전환 (선택사항)
- **물리적 제어**: 서보모터를 통해 실제 보일러 스위치 회전

## 🧩 구성 요소

| 구성 요소 | 역할 |
|---------|------|
| **스마트폰 웹 UI** | 사용자가 명령을 내리는 리모컨. Supabase DB의 값을 변경 |
| **Supabase (클라우드)** | 중앙 통제실. 데이터를 저장하고 변경 사항을 실시간 전송 |
| **라즈베리파이 제로 2W** | 집사(Controller). 클라우드의 명령을 받아 서보모터 제어 |
| **서보모터 (SG90)** | 물리적 손가락. 보일러 스위치를 실제로 회전시켜 모드 변경 |

## 🚀 설치 가이드

### 1. Supabase 설정

#### 1.1 데이터베이스 설정

Supabase 대시보드에서 SQL Editor를 열고 `supabase_setup.sql` 파일의 내용을 실행합니다:

```sql
-- 테이블 생성 및 Realtime 활성화
-- supabase_setup.sql 파일 참조
```

#### 1.2 Realtime 활성화 확인

Supabase 대시보드 > Database > Replication에서 `boiler_control` 테이블이 활성화되어 있는지 확인합니다.

#### 1.3 API 키 확인

Supabase 대시보드 > Settings > API에서 다음 정보를 확인합니다:
- Project URL
- anon/public key

### 2. 라즈베리파이 설정

**📌 상세 설치 가이드는 `raspberry_pi/INSTALL_GUIDE.md` 파일을 참조하세요!**

#### 빠른 시작

```bash
# 1. 파일 전송 (Git 또는 SCP 사용)
cd ~
git clone YOUR_REPOSITORY_URL house_heater
cd house_heater/raspberry_pi

# 2. 자동 설치 스크립트 실행
chmod +x install.sh
./install.sh

# 3. 환경 변수 설정
sudo nano /etc/systemd/system/boiler-controller.service
# SUPABASE_URL과 SUPABASE_KEY를 실제 값으로 수정

# 4. 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable boiler-controller.service
sudo systemctl start boiler-controller.service

# 5. 상태 확인
sudo systemctl status boiler-controller.service
```

#### 수동 설치

```bash
# pigpio 설치 (서보모터 제어를 위해 필요)
sudo apt update
sudo apt install -y pigpio python3-pip

# pigpio 데몬 시작 및 부팅 시 자동 시작 설정
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# Python 패키지 설치
pip3 install -r requirements.txt

# 환경 변수 설정 (서비스 파일 편집)
sudo nano /etc/systemd/system/boiler-controller.service
# SUPABASE_URL과 SUPABASE_KEY를 실제 값으로 수정

# 서비스 설치 및 시작
sudo cp boiler-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable boiler-controller.service
sudo systemctl start boiler-controller.service

# 로그 확인
sudo journalctl -u boiler-controller.service -f
```

### 3. 웹 UI 설정

#### 3.1 HTML 파일 편집

`web/index.html` 파일을 열어 다음 부분을 수정합니다:

```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL_HERE';
const SUPABASE_KEY = 'YOUR_SUPABASE_KEY_HERE';
const CORRECT_PIN = '1234'; // 원하는 PIN 번호로 변경
```

#### 3.2 웹 서버에 배포

**옵션 1: GitHub Pages**

1. GitHub 저장소 생성
2. `web/index.html` 파일 업로드
3. GitHub Pages 활성화
4. 배포된 URL로 접속

**옵션 2: Supabase Storage + Static Hosting**

1. Supabase Storage에 버킷 생성
2. `index.html` 파일 업로드
3. Public URL로 접속

**옵션 3: 로컬 웹 서버**

```bash
cd web
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000` 접속

## 📱 사용 방법

1. **웹 페이지 접속**: 스마트폰 브라우저에서 웹 UI URL 접속
2. **PIN 입력**: 4자리 PIN 번호 입력 (기본값: 1234)
3. **모드 선택**: 
   - **🔥 실내 난방 (0도)**: 실내 난방 모드로 전환
   - **💧 온수 전용 (60도)**: 온수 전용 모드로 전환
4. **상태 확인**: 화면 상단에서 현재 모드 확인

## 🔌 하드웨어 연결

### 서보모터 (SG90) 연결

| 서보모터 핀 | 라즈베리파이 핀 | 설명 |
|-----------|---------------|------|
| 빨간색 (VCC) | 5V (물리 핀 2번) | 전원 |
| 갈색/검은색 (GND) | GND (물리 핀 6번) | 접지 |
| 주황색 (Signal) | GPIO 18 (물리 핀 12번) | 제어 신호 |

### 서보모터 고정

- 핀 헤더가 없는 경우: 와이어를 구멍에 꽂고 글루건으로 고정
- 서보모터 본체도 글루건으로 라즈베리파이에 고정하여 반작용 방지

### 각도 조정

보일러 스위치의 실제 가동 범위에 맞게 각도를 조정해야 할 수 있습니다.

`raspberry_pi/boiler_controller.py` 파일에서 다음 값을 수정:

```python
ANGLE_0 = -1.0    # 0도 위치 (실제 보일러 0도 위치에 맞게 조정)
ANGLE_60 = 0.33   # 60도 위치 (실제 보일러 60도 위치에 맞게 조정)
```

## ⏰ 시간 예약 자동화 (선택사항)

자동화를 위한 여러 방법이 있습니다:

1. **GitHub Actions**: `supabase_schedule.sql` 파일의 주석 참조
2. **Vercel Cron**: Vercel의 Cron Jobs 기능 사용
3. **Supabase Edge Functions**: Edge Function + 외부 cron 서비스 조합

상세한 설정 방법은 `supabase_schedule.sql` 파일을 참조하세요.

## 🔧 문제 해결

### 서보모터가 작동하지 않음

1. **pigpio 데몬 확인**:
   ```bash
   sudo systemctl status pigpiod
   ```

2. **GPIO 연결 확인**: 핀 연결이 올바른지 확인

3. **전원 확인**: 서보모터가 충분한 전원을 공급받는지 확인

### Realtime 연결 실패

1. **Supabase 설정 확인**: Realtime이 활성화되어 있는지 확인
2. **네트워크 연결 확인**: 라즈베리파이가 인터넷에 연결되어 있는지 확인
3. **API 키 확인**: 환경 변수의 Supabase URL과 KEY가 올바른지 확인

### 로그 확인

```bash
# 서비스 로그 확인
sudo journalctl -u boiler-controller.service -f

# 파일 로그 확인
tail -f /var/log/boiler_controller.log
```

### 서비스 재시작

```bash
sudo systemctl restart boiler-controller.service
```

## 📁 프로젝트 구조

```
house_heater/
├── README.md                 # 이 파일
├── supabase_setup.sql        # Supabase 데이터베이스 설정
├── supabase_schedule.sql     # 시간 예약 자동화 설정
├── raspberry_pi/
│   ├── boiler_controller.py  # 라즈베리파이 제어 코드
│   ├── requirements.txt      # Python 패키지 목록
│   └── boiler-controller.service  # systemd 서비스 파일
└── web/
    └── index.html            # 모바일 웹 UI
```

## 🔒 보안 고려사항

1. **PIN 번호**: 프로덕션 환경에서는 더 강력한 인증 방식을 사용하세요
2. **API 키**: 서비스 키(service_role key)는 절대 클라이언트에 노출하지 마세요
3. **Row Level Security**: Supabase에서 RLS 정책을 설정하여 접근 제어를 강화하세요

## 📝 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

## 🤝 기여

버그 리포트나 개선 제안은 이슈로 등록해주세요.

