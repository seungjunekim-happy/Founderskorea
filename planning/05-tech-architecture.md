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
┌──────────────────────────────────────────────────────────────┐
│                     Railway (호스팅)                           │
│                                                               │
│  ┌───────────┐    ┌──────────────────────────────────────┐   │
│  │  Uvicorn   │───▶│          FastAPI App                 │   │
│  │  (ASGI)    │    │                                      │   │
│  └───────────┘    │  공개 라우트 ────────────────────────│   │
│                    │  ├── / (메인)                         │   │
│                    │  ├── /insights, /founders-voice       │   │
│                    │  ├── /weekly, /success-solution       │   │
│                    │  ├── /about, /contact, /newsletter    │   │
│                    │  ├── /search, /tags                   │   │
│                    │  └── /feed.xml, /sitemap.xml          │   │
│                    │                                      │   │
│                    │  관리자 라우트 (인증) ──────────────│   │
│                    │  ├── /admin (대시보드)                │   │
│                    │  ├── /admin/posts (CRUD)              │   │
│                    │  ├── /admin/submissions (투고 검토)   │   │
│                    │  └── /admin/weekly (큐레이션 관리)    │   │
│                    │                                      │   │
│                    │  서비스 레이어 ─────────────────────│   │
│                    │  ├── PostService                      │   │
│                    │  ├── SubmissionService                │   │
│                    │  ├── CurationService                  │   │
│                    │  ├── NewsletterService                │   │
│                    │  └── AuthService                      │   │
│                    │                                      │   │
│                    │  데이터 레이어 ─────────────────────│   │
│                    │  └── SQLAlchemy ORM                   │   │
│                    └────────────────┬─────────────────────┘   │
│                                     │                          │
│                    ┌────────────────▼─────────────────────┐   │
│                    │     PostgreSQL (Railway DB)           │   │
│                    │     ├── posts (모든 콘텐츠)           │   │
│                    │     ├── categories (4대 카테고리)     │   │
│                    │     ├── tags                          │   │
│                    │     ├── submissions (투고 대기열)     │   │
│                    │     ├── subscribers (뉴스레터)        │   │
│                    │     └── curated_news (스크래핑 데이터)│   │
│                    └──────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  스케줄러 (Weekly Curation)                           │    │
│  │  ├── 뉴스 스크래퍼 (requests + BeautifulSoup)        │    │
│  │  ├── 수집 → curated_news 테이블 저장                  │    │
│  │  └── 관리자 검토 후 발행                               │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
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
| 스크래핑 | requests + BeautifulSoup4 | Weekly Curation 뉴스 수집 |
| 스케줄링 | APScheduler 또는 cron | 주간 자동 수집 |
| 이메일 | Resend 또는 자체 SMTP | 뉴스레터 발송 |

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
│   │   ├── category.py           카테고리
│   │   ├── tag.py                태그
│   │   ├── submission.py         시민기자 투고
│   │   ├── curated_news.py       스크래핑 뉴스
│   │   └── subscriber.py         뉴스레터 구독자
│   ├── routers/                  라우트
│   │   ├── __init__.py
│   │   ├── home.py               메인 페이지
│   │   ├── insights.py           The Insights
│   │   ├── founders_voice.py     Founder's Voice + 투고
│   │   ├── weekly.py             Weekly Curation
│   │   ├── success_solution.py   Success Solution
│   │   ├── pages.py              소개, 상담, 뉴스레터 등
│   │   ├── search.py             검색
│   │   └── admin.py              관리자
│   ├── services/                 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── post_service.py
│   │   ├── submission_service.py
│   │   ├── curation_service.py
│   │   └── newsletter_service.py
│   ├── scraper/                  뉴스 스크래퍼
│   │   ├── __init__.py
│   │   ├── sources.py            뉴스 소스 정의
│   │   └── collector.py          수집 로직
│   └── utils/
│       ├── __init__.py
│       ├── markdown.py
│       ├── slug.py
│       └── seo.py
├── templates/
│   ├── base.html
│   ├── index.html                메인
│   ├── insights/
│   │   ├── list.html
│   │   └── detail.html
│   ├── founders_voice/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── submit.html
│   ├── weekly/
│   │   ├── list.html
│   │   └── detail.html
│   ├── success_solution/
│   │   ├── list.html
│   │   └── detail.html
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
-- 카테고리 (4개 고정)
categories: id, name, slug, description, color

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

-- 스크래핑 뉴스
curated_news: id, source_name, source_url, title, summary,
              scraped_at, is_selected, weekly_post_id

-- 구독자
subscribers: id, email, name, is_active, subscribed_at
```

## 6. 배포

- **개발**: 로컬 Uvicorn + SQLite
- **운영**: Railway + PostgreSQL
- **CI/CD**: GitHub push → Railway 자동 배포
- **환경 변수**: `DATABASE_URL`, `SECRET_KEY`, `ADMIN_PASSWORD`, `RESEND_API_KEY`
