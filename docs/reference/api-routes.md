# API 라우트 목록

> 모두 HTML 페이지 렌더링 라우트 (Jinja2 SSR). JSON API 엔드포인트는 별도 표기.

---

## 공개 페이지 라우트

| 메서드 | 경로 | 라우터 | 설명 |
|--------|------|--------|------|
| GET | `/` | `home.py` | 메인 페이지 (최신 포스트 + 카테고리 미리보기) |
| GET | `/about` | `pages.py` | 소개 페이지 |
| GET | `/contact` | `pages.py` | 상담 신청 폼 |
| GET | `/newsletter` | `pages.py` | 뉴스레터 구독 |

---

## 콘텐츠 카테고리

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/growth-playbook` | Growth Playbook 목록 |
| GET | `/ai-dx-lab` | AI/DX Lab 목록 |
| GET | `/founders-voice` | Founder's Voice 목록 |
| GET | `/success-cases` | Success Cases 목록 |
| GET | `/{category_slug}` | 카테고리별 포스트 목록 (`category.py`) |
| GET | `/{category_slug}/{post_slug}` | 포스트 상세 |

---

## 정부지원사업 (Gov-Support Radar)

| 메서드 | 경로 | 라우터 | 설명 |
|--------|------|--------|------|
| GET | `/gov-support` | `gov_support.py` | 정부지원사업 랜딩 페이지 |
| GET | `/gov-support/db` | `gov_support.py` | 지원사업 검색 DB (필터 UI) |
| GET | `/gov-support/{program_id}` | `gov_support.py` | 지원사업 상세 페이지 |

### 검색 파라미터 (`/gov-support/db`)

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `q` | string | 키워드 검색 |
| `region` | string | 지역 필터 |
| `industry` | string | 업종 필터 |
| `support_type` | string | 지원 유형 (자금/교육/멘토링 등) |
| `status` | string | 상태 (open/upcoming/closed) |
| `page` | int | 페이지 번호 (기본값 1) |

---

## 온보딩 퀴즈 (AI 매칭)

| 메서드 | 경로 | 라우터 | 설명 |
|--------|------|--------|------|
| GET | `/onboarding` | `onboarding.py` | 온보딩 퀴즈 페이지 |
| POST | `/onboarding/submit` | `onboarding.py` | 퀴즈 결과 제출 → AI 매칭 |
| GET | `/onboarding/result` | `onboarding.py` | 매칭 결과 페이지 |

---

## 유틸리티

| 메서드 | 경로 | 라우터 | 설명 |
|--------|------|--------|------|
| GET | `/feed.xml` | `feed.py` | RSS 피드 (전체) |
| GET | `/sitemap.xml` | `seo.py` | 사이트맵 XML |
| GET | `/robots.txt` | `seo.py` | 크롤러 설정 |

---

## 관리자 (미구현, Phase 2 예정)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/admin` | 관리자 대시보드 |
| GET/POST | `/admin/posts` | 포스트 CRUD |
| GET/POST | `/admin/gov-support` | 정부지원사업 DB 관리 |
| GET/POST | `/admin/submissions` | 투고 검토 |
