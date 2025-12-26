# 🚀 라즈베리파이 설치 및 실행 가이드

이 문서는 라즈베리파이 제로 2W에서 스마트 난방 조절기를 설치하고 실행하는 방법을 단계별로 설명합니다.

## 📋 준비 사항

- 라즈베리파이 제로 2W (또는 다른 라즈베리파이 모델)
- MicroSD 카드 (최소 8GB)
- 라즈베리파이 OS 설치 완료
- 인터넷 연결 (Wi-Fi 또는 이더넷)
- 서보모터 (SG90) 및 연결 케이블

---

## 1️⃣ 라즈베리파이 초기 설정

### SSH 접속 (권장)

```bash
# 라즈베리파이 IP 주소 확인 (라즈베리파이에서)
hostname -I

# PC/Mac에서 SSH 접속
ssh pi@라즈베리파이_IP주소
# 기본 비밀번호: raspberry (변경 권장)
```

### 시스템 업데이트

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 2️⃣ 프로젝트 파일 전송

### 방법 1: Git 사용 (권장)

```bash
# 라즈베리파이에서
cd ~
git clone YOUR_REPOSITORY_URL house_heater
cd house_heater
```

### 방법 2: SCP를 사용한 파일 전송

PC/Mac에서 실행:

```bash
# 프로젝트 디렉토리에서
scp -r raspberry_pi/* pi@라즈베리파이_IP주소:~/boiler_controller/
```

### 방법 3: USB 또는 직접 복사

1. MicroSD 카드를 PC에 연결
2. `raspberry_pi` 폴더를 복사
3. 라즈베리파이에서 접근

---

## 3️⃣ 필수 패키지 설치

### pigpio 설치 (서보모터 제어 필수)

```bash
# pigpio 설치
sudo apt install -y pigpio python3-pip

# pigpio 데몬 시작 및 부팅 시 자동 시작
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# 데몬 상태 확인
sudo systemctl status pigpiod
```

### Python 패키지 설치

```bash
# 작업 디렉토리로 이동
cd ~/boiler_controller

# Python 패키지 설치
pip3 install -r requirements.txt
```

**또는 설치 스크립트 사용:**

```bash
chmod +x install.sh
./install.sh
```

---

## 4️⃣ Supabase 환경 변수 설정

### 방법 1: systemd 서비스 파일에 직접 설정 (권장)

```bash
# 서비스 파일 편집
sudo nano /etc/systemd/system/boiler-controller.service
```

다음 부분을 실제 Supabase 값으로 수정:

```ini
Environment="SUPABASE_URL=https://your-project.supabase.co"
Environment="SUPABASE_KEY=your-anon-key-here"
```

**Supabase 정보 확인 방법:**
1. Supabase 대시보드 접속
2. Settings > API 메뉴
3. Project URL과 anon public key 복사

### 방법 2: 환경 변수 파일 사용 (선택사항)

```bash
# 환경 변수 파일 생성
nano ~/boiler_controller/.env
```

내용:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

그리고 systemd 서비스 파일에서:
```ini
EnvironmentFile=/home/pi/boiler_controller/.env
```

---

## 5️⃣ systemd 서비스 설정 및 시작

### 서비스 파일 복사

```bash
# 서비스 파일을 시스템 디렉토리로 복사
sudo cp ~/boiler_controller/boiler-controller.service /etc/systemd/system/

# 파일 권한 확인
sudo chmod 644 /etc/systemd/system/boiler-controller.service
```

### 서비스 파일 편집 (환경 변수 설정)

```bash
sudo nano /etc/systemd/system/boiler-controller.service
```

**중요: 다음 항목을 반드시 수정하세요!**

```ini
[Service]
User=pi                                    # 사용자명 확인 (기본값: pi)
WorkingDirectory=/home/pi/boiler_controller  # 실제 경로로 변경
Environment="SUPABASE_URL=YOUR_URL"        # 실제 URL 입력
Environment="SUPABASE_KEY=YOUR_KEY"        # 실제 KEY 입력
ExecStart=/usr/bin/python3 /home/pi/boiler_controller/boiler_controller.py  # 경로 확인
```

### 서비스 활성화 및 시작

```bash
# systemd 데몬 리로드
sudo systemctl daemon-reload

# 서비스 활성화 (부팅 시 자동 시작)
sudo systemctl enable boiler-controller.service

# 서비스 시작
sudo systemctl start boiler-controller.service

# 서비스 상태 확인
sudo systemctl status boiler-controller.service
```

### 로그 확인

```bash
# 실시간 로그 확인
sudo journalctl -u boiler-controller.service -f

# 최근 로그 50줄 확인
sudo journalctl -u boiler-controller.service -n 50

# 파일 로그 확인
tail -f /var/log/boiler_controller.log
```

---

## 6️⃣ 서비스 관리 명령어

### 서비스 제어

```bash
# 서비스 시작
sudo systemctl start boiler-controller.service

# 서비스 중지
sudo systemctl stop boiler-controller.service

# 서비스 재시작
sudo systemctl restart boiler-controller.service

# 서비스 상태 확인
sudo systemctl status boiler-controller.service

# 서비스 비활성화 (부팅 시 자동 시작 안 함)
sudo systemctl disable boiler-controller.service
```

### 문제 해결

```bash
# 서비스가 실행되지 않는 경우
sudo systemctl status boiler-controller.service

# 오류 확인
sudo journalctl -u boiler-controller.service --since "10 minutes ago"

# Python 스크립트 직접 실행 (테스트용)
cd ~/boiler_controller
export SUPABASE_URL="your-url"
export SUPABASE_KEY="your-key"
python3 boiler_controller.py
```

---

## 7️⃣ 수동 실행 방법 (테스트용)

서비스 없이 직접 실행하려면:

```bash
# 작업 디렉토리로 이동
cd ~/boiler_controller

# 환경 변수 설정
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-anon-key"

# 실행
python3 boiler_controller.py
```

**중지:** `Ctrl + C`

---

## 8️⃣ GPIO 연결 확인

서보모터 연결 확인:

| 서보모터 핀 | 라즈베리파이 핀 | 물리 번호 |
|------------|---------------|---------|
| 빨간색 (VCC) | 5V | 2번 |
| 갈색/검은색 (GND) | GND | 6번 |
| 주황색 (Signal) | GPIO 18 | 12번 |

연결 확인:
```bash
# GPIO 핀 상태 확인 (필요한 경우)
gpio readall

# 또는
pinout
```

---

## 9️⃣ 서보모터 각도 조정 (필수)

보일러 스위치의 실제 위치에 맞게 각도 조정:

```bash
# 코드 편집
nano ~/boiler_controller/boiler_controller.py
```

다음 부분을 수정:

```python
ANGLE_0 = -1.0    # 0도 위치 (실제 보일러 위치에 맞게 조정)
ANGLE_60 = 0.33   # 60도 위치 (실제 보일러 위치에 맞게 조정)
```

**테스트 방법:**
1. 각도를 조금씩 변경하면서 테스트
2. 실제 보일러 스위치 위치 확인
3. 최적의 각도 값 찾기

**각도 범위:**
- `-1.0` ~ `1.0` (gpiozero Servo 범위)
- `-1.0`: 0도 (왼쪽 끝)
- `0.0`: 90도 (중간)
- `1.0`: 180도 (오른쪽 끝)

---

## 🔟 최종 확인 체크리스트

- [ ] 라즈베리파이 OS 설치 완료
- [ ] 인터넷 연결 확인
- [ ] pigpio 설치 및 실행 중
- [ ] Python 패키지 설치 완료
- [ ] Supabase 환경 변수 설정 완료
- [ ] 서보모터 연결 확인 (GPIO 18)
- [ ] 서비스 파일 경로 및 환경 변수 확인
- [ ] systemd 서비스 활성화 및 실행 중
- [ ] 로그에 오류 없음 확인
- [ ] Supabase DB 초기화 완료 (supabase_setup.sql 실행)
- [ ] 웹 UI에서 모드 변경 테스트

---

## 🐛 자주 발생하는 문제

### 1. "Permission denied" 오류

```bash
# 파일 실행 권한 부여
chmod +x boiler_controller.py

# 로그 디렉토리 권한 확인
sudo mkdir -p /var/log
sudo touch /var/log/boiler_controller.log
sudo chmod 666 /var/log/boiler_controller.log
```

### 2. "pigpio not running" 오류

```bash
# pigpio 데몬 확인 및 재시작
sudo systemctl status pigpiod
sudo systemctl restart pigpiod
```

### 3. "Supabase 연결 실패" 오류

```bash
# 환경 변수 확인
sudo systemctl show boiler-controller.service | grep Environment

# 수동으로 환경 변수 확인
printenv | grep SUPABASE
```

### 4. "GPIO 18 사용 중" 오류

```bash
# 다른 프로세스 종료
sudo pkill -f boiler_controller
sudo systemctl restart boiler-controller.service
```

---

## 📝 다음 단계

1. **웹 UI 설정**: `web/index.html`에서 Supabase URL/KEY 설정
2. **PIN 번호 변경**: 웹 UI의 PIN 번호를 보안을 위해 변경
3. **각도 정밀 조정**: 실제 보일러 스위치 위치에 맞게 각도 미세 조정
4. **시간 예약 설정**: `supabase_schedule.sql` 참고하여 자동화 설정

---

## 💡 팁

- **로그 모니터링**: 서비스 실행 후 로그를 지속적으로 모니터링하여 문제 조기 발견
- **백업**: 설정 파일을 정기적으로 백업
- **테스트**: 실제 보일러에 연결하기 전에 서보모터만 테스트
- **안전**: 전원 차단 후 하드웨어 작업 진행

