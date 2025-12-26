# 🔧 pigpio 설치 문제 해결 방법

Debian Trixie에서는 시스템 패키지 `pigpio`가 기본 저장소에 없을 수 있습니다.

## ✅ 해결 방법

### 방법 1: 수정된 설치 스크립트 사용 (권장)

코드가 이미 수정되어 있어서 `pigpio` 시스템 패키지 없이도 작동합니다:

```bash
# 수정된 install.sh 실행
chmod +x install.sh
./install.sh
```

이제 `pigpio` 시스템 패키지가 없어도 Python 패키지만으로 작동합니다.

---

### 방법 2: 수동 설치 (pigpio 시스템 패키지 없이)

```bash
# 기본 패키지만 설치
sudo apt update
sudo apt install -y python3-pip git python3-dev gcc

# Python 패키지 설치 (pigpio Python 패키지 포함)
pip3 install -r requirements.txt

# 나머지 설치 계속 진행
cd ~/boiler_controller
# ... 나머지 설정
```

---

### 방법 3: 소스에서 pigpio 빌드 (고급 사용자)

만약 시스템 패키지가 반드시 필요한 경우:

```bash
# 의존성 설치
sudo apt install -y build-essential python3-dev

# 소스 다운로드 및 빌드
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install

# 데몬 시작
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

하지만 **방법 1이 가장 간단하고 권장됩니다!**

---

## 📝 변경 사항

코드가 수정되어:
- `pigpio` 시스템 패키지가 없어도 작동
- Python 패키지 `pigpio`만으로도 동작 (gpiozero 기본 팩토리 사용)
- 더 유연하고 호환성이 좋아짐

---

## ✅ 확인

설치 후 테스트:

```bash
# Python 스크립트 직접 실행
cd ~/boiler_controller
export SUPABASE_URL="https://ajtjxkngstbzbjhvtkdr.supabase.co"
export SUPABASE_KEY="sb_publishable_CEWJ_yVJQQOGHpAK43dhJQ_X0bIkX6h"
python3 boiler_controller.py
```

오류 없이 시작되면 성공!

