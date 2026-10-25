# 정보꾸러미 인사이트 — Astro 기본 블로그

테마 없이 Astro로 직접 구성한 미니멀 블로그 시작 프로젝트입니다.

## 포함된 기능

- 흰 배경과 얇은 구분선 중심의 반응형 디자인
- 상단 메뉴: 건강, 생활 정보, 뉴스, 기타
- 하단 메뉴: 블로그 소개, 개인정보처리방침, 문의
- Markdown 기반 글 목록 및 상세 페이지
- 카테고리별 페이지
- 최근 글 목록 및 관련 글
- SEO 기본 메타 태그와 canonical URL
- `@astrojs/sitemap` 기반 사이트맵
- 엑셀 → Python → Markdown 생성 스크립트

## 1. 설치 및 로컬 실행

Node.js LTS를 설치한 후 프로젝트 폴더에서 실행합니다.

```bash
npm install
npm run dev
```

브라우저에서 터미널에 표시되는 로컬 주소를 엽니다.

## 2. 실제 도메인 설정

`astro.config.mjs`에서 `site`를 실제 도메인으로 변경합니다.

`public/robots.txt`의 Sitemap 주소도 같은 도메인으로 변경하세요.
현재 `https://example.com`은 예시 주소입니다.

## 3. 글 추가

`src/content/posts/`에 `.md` 파일을 추가합니다. `sample-health.md`는 구조 예시이며 `draft: true`라서 공개 목록에 표시되지 않습니다.

## 4. 엑셀에서 글 생성

필요한 Python 패키지를 설치합니다.

```bash
pip install pandas openpyxl
```

엑셀을 `input/posts.xlsx`에 넣고 실행합니다.

```bash
python scripts/generate_posts.py
```

다른 경로의 엑셀 파일을 지정할 수도 있습니다.

```bash
python scripts/generate_posts.py "C:/경로/posts.xlsx"
```

스크립트는 기존 파일을 덮어쓰지 않습니다. 파일을 수정해야 한다면 먼저 기존 Markdown을 백업한 뒤 수동으로 수정하거나 별도 업데이트 절차를 마련하세요.

## 5. Cloudflare Pages 설정

GitHub 저장소를 Cloudflare Pages에 연결할 때 일반적인 설정은 다음과 같습니다.

- Framework preset: Astro 또는 None
- Build command: `npm run build`
- Build output directory: `dist`
- Node.js 버전: Cloudflare 빌드 환경에서 지원되는 LTS 버전

## 배포 전 확인 사항

- `astro.config.mjs`와 `public/robots.txt`의 예시 도메인을 실제 도메인으로 변경
- 문의 페이지의 이메일 주소 입력
- 개인정보처리방침을 실제 쿠키·광고·통계 도구 사용 현황에 맞게 수정
- `npm run build`로 빌드 확인
- 글 제목·본문·출처와 이미지 사용 권한 검수
- Google Search Console 및 네이버 서치어드바이저 등록

이 프로젝트는 시작용 기본 구조입니다. 검색 노출이나 색인 여부를 보장하지 않습니다.
