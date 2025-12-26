# 🚀 Vercel 배포 가이드

웹 UI를 Vercel에 배포하는 방법입니다.

---

## 방법 1: Vercel 웹 인터페이스 사용 (가장 쉬움)

### 1단계: Vercel 접속 및 로그인

1. https://vercel.com 접속
2. GitHub 계정으로 로그인 (또는 이메일로 가입)

### 2단계: 새 프로젝트 추가

1. 대시보드에서 **Add New...** → **Project** 클릭
2. GitHub 저장소에서 **house-controller** 선택
3. 또는 **Import Third-Party Git Repository** 클릭

### 3단계: 프로젝트 설정

- **Framework Preset**: Other
- **Root Directory**: `web` 선택 (중요!)
- **Build Command**: (비워두기)
- **Output Directory**: (비워두기)

### 4단계: 배포

1. **Deploy** 버튼 클릭
2. 몇 초 후 배포 완료!
3. 생성된 URL 확인 (예: `https://house-controller-xxxx.vercel.app`)

---

## 방법 2: Vercel CLI 사용 (터미널)

### 1단계: Vercel CLI 설치

```bash
npm install -g vercel
```

또는 `npx vercel` 사용 (설치 없이)

### 2단계: 웹 디렉토리로 이동 및 배포

```bash
cd "/Users/choieuro/Library/Mobile Documents/com~apple~CloudDocs/01_Project/01_Success/house_heater/web"
vercel
```

### 3단계: 배포 설정

- 첫 배포 시:
  - `Set up and deploy?` → **Y** 입력
  - `Which scope?` → 계정 선택
  - `Link to existing project?` → **N** (새 프로젝트)
  - `What's your project's name?` → `house-controller-web` (또는 원하는 이름)
  - `In which directory is your code located?` → `./` 또는 Enter
  - `Want to override the settings?` → **N**

### 4단계: 배포 완료

배포 완료 후 URL이 표시됩니다!

---

## 방법 3: GitHub 연동 (자동 배포)

### 1단계: Vercel에서 GitHub 저장소 연결

1. Vercel 대시보드 → **Add New...** → **Project**
2. GitHub 저장소 **house-controller** 선택
3. 프로젝트 설정:
   - **Root Directory**: `web`
   - **Framework Preset**: Other

### 2단계: 자동 배포 설정

- GitHub에 푸시할 때마다 자동으로 재배포됩니다
- `main` 브랜치에 푸시하면 프로덕션 배포
- 다른 브랜치에 푸시하면 프리뷰 배포

---

## ✅ 배포 확인

1. 생성된 Vercel URL 접속
2. PIN 입력 화면이 나타나는지 확인
3. Supabase 연결 테스트 (버튼 클릭)

---

## 🔄 재배포

### 수동 재배포 (CLI)

```bash
cd web
vercel --prod
```

### 자동 재배포 (GitHub 연동 시)

```bash
git add .
git commit -m "웹 UI 업데이트"
git push origin main
```

Vercel이 자동으로 재배포합니다!

---

## 🔧 커스텀 도메인 설정 (선택사항)

1. Vercel 프로젝트 설정 → **Domains**
2. 원하는 도메인 추가
3. DNS 설정 가이드 따라하기

---

## 📝 참고사항

- **Root Directory**: `web` 폴더를 지정해야 합니다
- **빌드 불필요**: 정적 HTML 파일이므로 빌드 과정이 필요 없습니다
- **무료 플랜**: 충분히 사용 가능합니다 (무료 배포 가능)

---

## 🐛 문제 해결

### "Cannot find index.html"

- Root Directory를 `web`으로 설정했는지 확인
- 또는 프로젝트 루트에 `vercel.json` 파일 추가

### 배포는 되지만 페이지가 보이지 않음

- URL 끝에 `/index.html`을 추가해보세요
- 또는 `vercel.json` 파일 확인

### Supabase 연결 오류

- 브라우저 개발자 도구(F12) → Console에서 오류 확인
- Supabase URL/KEY가 올바른지 확인
- CORS 설정 확인 (Supabase에서는 기본적으로 허용됨)

