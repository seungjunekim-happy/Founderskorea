# The Founders Korea 기술 아키텍처

## 1. 현재 아키텍처

```
┌─────────────────────────────────────────┐
│              Railway (호스팅)             │
│                                         │
│  ┌───────────┐    ┌──────────────────┐  │
│  │  Uvicorn   │───▶│   FastAPI App    │  │
│  │  (ASGI)    │    │  main.py         │  │
│  └───────────┘    │  ├── 라우트 3개   │  │
│                    │  ├── 하드코딩 데이터│ │
│                    │  └── Jinja2 렌더링 │  │
│                    └───────┬──────────┘  │
│                    ┌───────▼──────────┐  │
│                    │  Templates + CSS  │  │
│                    └──────────────────┘  │
└─────────────────────────────────────────┘
```

## 2. 목표 아키텍처

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Railway (호스팅)                                  │
│                                                                            │
│  ┌───────────┐    ┌──────────────────────────────────────────────────┐   │
│  │  Uvicorn   │───▶│               FastAPI App                        │   │
│  │  (ASGI)    │    │                                                  │   │
│  └───────────┘    │  공개 라우트 ──────────────────────────────────  │   │
│                    │  ├── / (메인)                                    │   │
│                    │  ├── /growth-playbook (성장 플레이북)            │   │
│                    │  ├── /ai-dx-lab (AI/DX 연구소)                   │   │
│                    │  ├── /founders-voice (파운더스 보이스 + 투고)    │   │
│                    │  ├── /gov-support (정부지원 레이더)               │   │
│                    │  ├── /gov-support/db (정부지원 DB 검색)           │   │
│                    │  ├── /success-cases (성공사례)                    │   │
│                    │  ├── /digital-products (디지털 상품 스토어)       │   │
│                    │  ├── /about, /contact, /newsletter               │   │
│                    │  ├── /search, /tags                              │   │
│                    │  └── /feed.xml, /sitemap.xml                     │   │
│                    │                                                  │   │
│                    │  관리자 라우트 (인증) ────────────────────────  │   │
│                    │  ├── /admin (대시보드)                           │   │
│                    │  ├── /admin/posts (CRUD)                         │   │
│                    │  ├── /admin/submissions (투고 검토)              │   │
│                    │  ├── /admin/gov-support (정부지원 DB 관리)       │   │
│                    │  └── /admin/digital-products (상품 관리)         │   │
│                    │                                                  │   │
│                    │  서비스 레이어 ──────────────────────────────  │   │
│                    │  ├── PostService                                 │   │
│                    │  ├── SubmissionService                           │   │
│                    │  ├── GovSupportService (정부지원 검색/필터)      │   │
│                    │  ├── AIMatchingService (프로필 기반 매칭 점수)   │   │
│                    │  ├── ReviewService (리뷰 CRUD + 통계)           │   │
│                    │  ├── DigitalProductService (Phase 3)             │   │
│                    │  ├── NewsletterService                           │   │
│                    │  └── AuthService                                 │   │
│                    │                                                  │   │
│                    │  데이터 레이어 ──────────────────────────────  │   │
│                    │  └── SQLAlchemy ORM                              │   │
│                    └────────────────┬─────────────────────────────────┘   │
│                                     │                                      │
│                    ┌────────────────▼─────────────────────────────────┐   │
│                    │        PostgreSQL (Railway DB)                    │   │
│                    │  ├── posts (모든 콘텐츠)                          │   │
│                    │  ├── categories (5대 카테고리)                    │   │
│                    │  ├── tags, post_tags                              │   │
│                    │  ├── submissions (투고 대기열)                    │   │
│                    │  ├── subscribers (뉴스레터)                       │   │
│                    │  ├── gov_support_programs (정부지원 DB)           │   │
│                    │  ├── gov_support_alerts (맞춤 알림)               │   │
│                    │  ├── user_profiles (사용자 프로필/온보딩)         │   │
│                    │  ├── program_reviews (프로그램 리뷰)              │   │
│                    │  ├── application_kits (신청 키트)                 │   │
│                    │  ├── digital_products (디지털 상품, Phase 3)      │   │
│                    │  └── orders (주문 내역, Phase 3)                  │   │
│                    └──────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  Gov-Support Scraper (정부지원 자동 수집)                         │    │
│  │  ├── 공공데이터포털 API (httpx/aiohttp로 비동기 호출)            │    │
│  │  ├── 창업진흥원, K-Startup, 중기부 웹 스크래핑                   │    │
│  │  ├── AI 큐레이션 (OpenAI/Claude API로 자동 검수/분류)            │    │
│  │  ├── gov_support_programs 테이블 자동 업데이트                   │    │
│  │  └── 스케줄러 (일 1회 실행)                                       │    │
│  └──────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
```

## 3. 기술 스택

### 현재
| 영역 | 기술 | 버전 |
|------|------|------|
| 백엔드 | FastAPI | 0.115.6 |
| ASGI 서버 | Uvicorn | 0.34.0 |
| 템플릿 | Jinja2 | 3.1.5 |
| 배포 | Railway + Docker | - |

### 도입 예정
| 영역 | 기술 | 용도 |
|------|------|------|
| ORM | SQLAlchemy 2.0 | 데이터베이스 관리 |
| 마이그레이션 | Alembic | DB 스키마 버전 관리 |
| DB (개발) | SQLite | 로컬 개발 |
| DB (운영) | PostgreSQL | Railway DB |
| 마크다운 | python-markdown | 포스트 본문 렌더링 |
| 인증 | PyJWT | 관리자 인증 |
| 환경변수 | python-dotenv | 설정 관리 |
| 스크래핑 | requests + BeautifulSoup4 | 웹 스크래핑 |
| 비동기 HTTP | httpx 또는 aiohttp | 공공데이터포털 API 호출 |
| 스케줄링 | APScheduler 또는 cron | 일간 자동 수집 |
| 이메일 | Resend 또는 자체 SMTP | 뉴스레터 발송 |
| AI API | OpenAI/Claude API | 정부지원 큐레이션/검수 자동화 |
| AI 매칭 | OpenAI/Claude API | 사용자 프로필 기반 정부지원 매칭 점수 |
| 결제 (Phase 3) | 토스페이먼츠 또는 Stripe | Freemium 이후 수익화 시 도입 |

## 4. 프로젝트 구조 (목표)

```
Founderskorea/
├── main.py                       앱 진입점
├── app/
│   ├── __init__.py
│   ├── config.py                 환경설정
│   ├── database.py               DB 연결
│   ├── models/                   SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── post.py               포스트 (전체 카테고리 공용)
│   │   ├── category.py           카테고리 (5개 고정)
│   │   ├── tag.py                태그
│   │   ├── submission.py         시민기자 투고
│   │   ├── subscriber.py         뉴스레터 구독자
│   │   ├── gov_support_program.py    정부지원 프로그램
│   │   ├── user_profile.py          사용자 프로필 (온보딩 퀴즈)
│   │   ├── program_review.py        프로그램 리뷰
│   │   ├── application_kit.py       신청 키트
│   │   └── digital_product.py       디지털 상품 (Phase 3)
│   ├── routers/                  라우트
│   │   ├── __init__.py
│   │   ├── home.py               메인 페이지
│   │   ├── growth_playbook.py    성장 플레이북
│   │   ├── ai_dx_lab.py          AI/DX 연구소
│   │   ├── founders_voice.py     파운더스 보이스 + 투고
│   │   ├── gov_support.py        정부지원 레이더 + DB 검색
│   │   ├── success_cases.py      성공사례
│   │   ├── digital_products.py   디지털 상품 스토어
│   │   ├── pages.py              소개, 상담, 뉴스레터 등
│   │   ├── search.py             검색
│   │   └── admin.py              관리자
│   ├── services/                 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── post_service.py
│   │   ├── submission_service.py
│   │   ├── gov_support_service.py     정부지원 검색/필터
│   │   ├── ai_matching_service.py    사용자 프로필 기반 AI 매칭
│   │   ├── review_service.py         프로그램 리뷰 CRUD + 통계
│   │   ├── digital_product_service.py  상품 관리/주문 (Phase 3)
│   │   └── newsletter_service.py
│   ├── scraper/                  자동 수집기
│   │   ├── __init__.py
│   │   ├── sources.py            정부지원 소스 정의
│   │   ├── collector.py          수집 로직
│   │   └── gov_api.py            공공데이터포털 API 클라이언트
│   └── utils/
│       ├── __init__.py
│       ├── markdown.py
│       ├── slug.py
│       ├── seo.py
│       └── ai_curator.py         AI 큐레이션 헬퍼
├── templates/
│   ├── base.html
│   ├── index.html                메인
│   ├── growth_playbook/
│   │   ├── list.html
│   │   └── detail.html
│   ├── ai_dx_lab/
│   │   ├── list.html
│   │   └── detail.html
│   ├── founders_voice/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── submit.html
│   ├── gov_support/
│   │   ├── list.html
│   │   ├── db.html               정부지원 DB 검색
│   │   └── alert.html            맞춤 알림 설정
│   ├── success_cases/
│   │   ├── list.html
│   │   └── detail.html
│   ├── digital_products/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── checkout.html
│   ├── pages/
│   │   ├── about.html
│   │   ├── contact.html
│   │   └── newsletter.html
│   ├── search.html
│   ├── admin/                    관리자 템플릿
│   └── 404.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── alembic/
├── planning/
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
```

## 5. DB 스키마 (핵심)

```sql
-- 카테고리 (5개 고정)
categories: id, name, slug, description, color
  - Growth Playbook (성장 플레이북)
  - AI/DX Lab (AI/DX 연구소)
  - Founder's Voice (파운더스 보이스)
  - Gov-Support Radar (정부지원 레이더)
  - Success Cases (성공사례)

-- 포스트 (전체 콘텐츠 통합)
posts: id, title, slug, summary, content, category_id,
       author_name, author_info, is_published, is_featured,
       created_at, updated_at

-- 태그
tags: id, name, slug
post_tags: post_id, tag_id

-- 시민기자 투고 (검토 대기열)
submissions: id, author_name, author_business, author_email,
             title, content, status(pending/approved/rejected),
             submitted_at, reviewed_at

-- 뉴스레터 구독자
subscribers: id, email, name, is_active, subscribed_at

-- 정부지원 프로그램 DB (신규)
gov_support_programs:
  - id: 고유 ID
  - title: 사업명
  - organization: 주관기관
  - apply_start: 신청 시작일
  - apply_end: 신청 마감일
  - target_industry: 대상 업종 (JSON 배열)
  - target_region: 대상 지역 (JSON 배열)
  - target_scale: 대상 규모 (예비창업, 초기, 성장기 등)
  - support_type: 지원 유형 (자금, 교육, 멘토링, 공간 등)
  - support_amount: 지원 규모 (최대 금액)
  - apply_method: 신청 방법 (URL)
  - source_url: 원본 공고 URL
  - tags: 키워드 (JSON 배열)
  - status: 상태 (upcoming/open/closed)
  - scraped_at: 수집 시각
  - updated_at: 업데이트 시각

-- 정부지원 맞춤 알림 (신규)
gov_support_alerts:
  - id: 고유 ID
  - subscriber_id: 구독자 ID (subscribers 연결)
  - keywords: 관심 키워드 (JSON 배열)
  - regions: 관심 지역 (JSON 배열)
  - industries: 관심 업종 (JSON 배열)
  - created_at: 생성 시각

-- 사용자 프로필 / 온보딩 퀴즈 (신규 - Phase 1)
user_profiles:
  - id: 고유 ID
  - session_id: 세션 ID (비회원) 또는 email (회원)
  - industry: 업종 (예: IT, 제조, 서비스, F&B 등)
  - business_stage: 창업 단계 (예비창업, 초기, 성장기, 성숙기)
  - business_scale: 사업 규모 (1인, 5인 이하, 10인 이하, 50인 이하 등)
  - region: 지역 (서울, 경기, 부산 등)
  - interests: 관심 분야 (JSON 배열 - 자금, R&D, 교육, 공간, 판로 등)
  - created_at: 생성 시각

-- 프로그램 리뷰 (신규 - Phase 1)
program_reviews:
  - id: 고유 ID
  - program_id: 프로그램 ID (gov_support_programs FK)
  - reviewer_name: 작성자 이름
  - rating: 별점 (1~5)
  - review_text: 리뷰 본문
  - success_tag: 결과 태그 (success/failure/in_progress)
  - tips: 신청 팁
  - created_at: 작성 시각

-- 신청 키트 (신규 - Phase 1)
application_kits:
  - id: 고유 ID
  - program_id: 프로그램 ID (gov_support_programs FK)
  - title: 키트 제목
  - content: 마크다운 본문 (서류 준비 가이드, 사업계획서 팁 등)
  - checklist: 체크리스트 (JSON 배열)
  - download_count: 다운로드 횟수
  - created_at: 생성 시각

-- 디지털 상품 (Phase 3으로 이동)
digital_products:
  - id: 고유 ID
  - title: 상품명
  - description: 상품 설명
  - price: 가격
  - file_url: 파일 다운로드 URL (보안 처리)
  - category: 카테고리 (템플릿, 가이드북 등)
  - download_count: 다운로드 횟수
  - created_at: 생성 시각

-- 주문 내역 (신규)
orders:
  - id: 고유 ID
  - product_id: 상품 ID (digital_products 연결)
  - buyer_email: 구매자 이메일
  - buyer_name: 구매자 이름
  - amount: 결제 금액
  - payment_status: 결제 상태 (pending/completed/failed)
  - created_at: 주문 시각
```

## 6. 배포

- **개발**: 로컬 Uvicorn + SQLite
- **운영**: Railway + PostgreSQL
- **CI/CD**: GitHub push → Railway 자동 배포
- **환경 변수**:
  - `DATABASE_URL`: PostgreSQL 연결 문자열
  - `SECRET_KEY`: JWT 서명 키
  - `ADMIN_PASSWORD`: 관리자 암호 해시
  - `RESEND_API_KEY`: 이메일 발송 키
  - `OPENAI_API_KEY` 또는 `ANTHROPIC_API_KEY`: AI 큐레이션 API
  - `GOV_DATA_API_KEY`: 공공데이터포털 API 키
  - `PAYMENT_API_KEY`: 결제 API 키 (Phase 3 Freemium 이후)
