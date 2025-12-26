# 📤 GitHub 업로드 가이드

## 1️⃣ GitHub 저장소 생성

1. https://github.com 접속
2. 오른쪽 상단 **+** 버튼 클릭 → **New repository** 선택
3. 다음 정보 입력:
   - **Repository name**: `house-controller`
   - **Description**: `라즈베리파이와 Supabase를 활용한 스마트 난방 조절기`
   - **Visibility**: ⚪ **Private** 선택 (중요!)
   - **Initialize this repository with**: 모두 체크 해제 (이미 로컬에 파일이 있음)
4. **Create repository** 클릭

## 2️⃣ GitHub에 푸시

저장소 생성 후 표시되는 명령어를 실행하거나, 아래 명령어를 사용하세요:

```bash
cd "/Users/choieuro/Library/Mobile Documents/com~apple~CloudDocs/01_Project/01_Success/house_heater"

# GitHub 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/house-controller.git

# main 브랜치로 푸시
git push -u origin main
```

**또는 SSH를 사용하는 경우:**

```bash
git remote add origin git@github.com:YOUR_USERNAME/house-controller.git
git push -u origin main
```

## 3️⃣ 완료 확인

GitHub 저장소 페이지에서 모든 파일이 업로드되었는지 확인하세요.

## ⚠️ 보안 참고사항

현재 프로젝트에 Supabase KEY가 포함되어 있습니다:
- `web/index.html` - Supabase URL/KEY 포함
- `raspberry_pi/boiler-controller.service` - Supabase URL/KEY 포함

**Private 저장소**로 설정했으므로 일반 사용자는 접근할 수 없지만, 다음 사항을 고려하세요:

1. 저장소 접근 권한 관리
2. 필요시 GitHub Secrets 사용 고려
3. 향후 Public으로 변경 시 키 제거 필요

