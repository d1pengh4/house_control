# ✅ Supabase 설정 완료

Supabase 연결 정보가 프로젝트 파일에 설정되었습니다.

## 📋 설정된 정보

- **URL**: `https://ajtjxkngstbzbjhvtkdr.supabase.co`
- **KEY**: `sb_publishable_CEWJ_yVJQQOGHpAK43dhJQ_X0bIkX6h`

## 🔧 설정이 적용된 파일

1. **웹 UI**: `web/index.html`
   - Supabase URL과 KEY가 설정되어 바로 사용 가능합니다.

2. **라즈베리파이 서비스**: `raspberry_pi/boiler-controller.service`
   - 환경 변수가 설정되어 있습니다.
   - 라즈베리파이에 복사하여 사용하세요.

## ⚠️ 다음 단계

### 1. Supabase 데이터베이스 초기화

Supabase 대시보드에서 SQL Editor를 열고 `supabase_setup.sql` 파일의 내용을 실행하세요:

```sql
-- supabase_setup.sql 파일의 모든 SQL 명령어 실행
```

### 2. 라즈베리파이 설정

```bash
# 라즈베리파이에서
cd ~/boiler_controller

# 서비스 파일 복사 (이미 Supabase 정보가 설정되어 있음)
sudo cp boiler-controller.service /etc/systemd/system/

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable boiler-controller.service
sudo systemctl start boiler-controller.service
```

### 3. 웹 UI 배포

`web/index.html` 파일을 웹 서버에 업로드하거나 GitHub Pages 등에 배포하세요.

### 4. PIN 번호 변경 (보안)

기본 PIN 번호 `1234`를 더 안전한 번호로 변경하는 것을 권장합니다:

- **웹 UI**: `web/index.html` 파일에서 `CORRECT_PIN` 값 변경

## 🔒 보안 권장사항

1. **Git 저장소에 업로드 시 주의**
   - 실제 키가 포함된 파일을 public 저장소에 올리지 마세요.
   - `.gitignore` 파일에 민감한 정보가 포함된 파일을 추가하세요.

2. **PIN 번호 변경**
   - 기본 PIN `1234`를 더 복잡한 번호로 변경하세요.

3. **Supabase RLS (Row Level Security) 설정**
   - Supabase 대시보드에서 RLS 정책을 설정하여 접근 제어를 강화하세요.

## ✅ 체크리스트

- [x] Supabase URL 설정 완료
- [x] Supabase KEY 설정 완료
- [ ] Supabase 데이터베이스 초기화 (`supabase_setup.sql` 실행)
- [ ] 라즈베리파이 서비스 설치 및 시작
- [ ] 웹 UI 배포
- [ ] PIN 번호 변경 (선택사항)
- [ ] 테스트 실행

## 🐛 문제 해결

### "Invalid API key" 오류

- Supabase 대시보드에서 API 키가 올바른지 확인하세요.
- Settings > API 메뉴에서 anon/public key를 확인하세요.

### 연결 실패

- 라즈베리파이의 인터넷 연결을 확인하세요.
- Supabase 프로젝트가 활성화되어 있는지 확인하세요.

