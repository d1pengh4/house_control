#!/bin/bash
# pigpio 문제 해결 버전 설치 스크립트

set -e

echo "=== 스마트 난방 조절기 설치 시작 ==="

# 1. 필요한 시스템 패키지 설치 (pigpio 제외)
echo "1. 시스템 패키지 설치 중..."
sudo apt update
sudo apt install -y python3-pip git python3-dev gcc

# 2. Python 패키지 설치
echo "2. Python 패키지 설치 중..."
pip3 install -r requirements.txt

# 3. 작업 디렉토리 생성
WORK_DIR="/home/$(whoami)/boiler_controller"
echo "3. 작업 디렉토리 생성: $WORK_DIR"
mkdir -p "$WORK_DIR"

# 현재 스크립트 위치에서 파일 복사
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/boiler_controller.py" "$WORK_DIR/"
cp "$SCRIPT_DIR/requirements.txt" "$WORK_DIR/"

# 5. 실행 권한 부여
chmod +x "$WORK_DIR/boiler_controller.py"

# 6. 서비스 파일 복사 및 설정 안내
echo "4. 서비스 파일 준비 중..."
cp "$SCRIPT_DIR/boiler-controller.service" "$WORK_DIR/"

echo ""
echo "=== 설치 완료 ==="
echo ""
echo "다음 단계를 수행하세요:"
echo ""
echo "1. Supabase 정보 확인 (서비스 파일에 이미 설정되어 있음)"
echo "   cat $WORK_DIR/boiler-controller.service | grep SUPABASE"
echo ""
echo "2. 서비스 파일을 시스템 디렉토리로 복사:"
echo "   sudo cp $WORK_DIR/boiler-controller.service /etc/systemd/system/"
echo ""
echo "3. 서비스 활성화 및 시작:"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable boiler-controller.service"
echo "   sudo systemctl start boiler-controller.service"
echo ""
echo "4. 서비스 상태 확인:"
echo "   sudo systemctl status boiler-controller.service"
echo ""
echo "5. 로그 확인:"
echo "   sudo journalctl -u boiler-controller.service -f"
echo ""

