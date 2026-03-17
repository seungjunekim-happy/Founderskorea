# 기술 아키텍처

> 원본 상세 문서: [planning/05-tech-architecture.md](../../planning/05-tech-architecture.md)

---

## 기술 스택

### 현재 운영 중

| 영역 | 기술 | 버전 |
|------|------|------|
| 백엔드 | FastAPI | 0.115.6 |
| ASGI 서버 | Uvicorn | 0.34.0 |
| 템플릿 | Jinja2 | 3.1.5 |
| ORM | SQLAlchemy | 2.0.36 |
| 마이그레이션 | Alembic | 1.14.1 |
| DB (개발) | SQLite + aiosqlite | — |
| DB (운영) | PostgreSQL (Railway) | — |
| 마크다운 | python-markdown + Pygments | 3.7 / 2.19.1 |
| 배포 | Railway + Docker | — |

### 도입 예정

| 영역 | 기술 | 용도 |
|------|------|------|
| 인증 | PyJWT | 관리자 인증 |
| 비동기 HTTP | httpx / aiohttp | 공공데이터포털 API 호출 |
| 스케줄링 | APScheduler | 정부지원사업 일간 자동 수집 |
| 이메일 | Resend | 뉴스레터 발송 |
| AI API | OpenAI / Anthropic | 정부지원사업 매칭 점수 |
| 결제 | 토스페이먼츠 / Stripe | Phase 3 수익화 시 도입 |

---

## 앱 구조

```
Founderskorea/
├── main.py                  앱 진입점
├── app/
│   ├── config.py            환경설정 (pydantic-settings)
│   ├── database.py          DB 연결 (SQLAlchemy async)
│   ├── dependencies.py      FastAPI 의존성
│   ├── models/              SQLAlchemy 모델
│   │   ├── post.py
│   │   ├── category.py
│   │   ├── gov_support.py
│   │   └── user.py
│   ├── routers/             페이지 라우트 (HTML 렌더링)
│   │   ├── home.py          메인 페이지
│   │   ├── category.py      카테고리별 목록/상세
│   │   ├── gov_support.py   정부지원사업 랜딩 + DB 검색
│   │   ├── onboarding.py    AI 매칭 퀴즈
│   │   ├── pages.py         소개, 상담, 뉴스레터 등
│   │   ├── feed.py          RSS 피드
│   │   └── seo.py           sitemap.xml, robots.txt
│   ├── services/            비즈니스 로직
│   │   ├── gov_support_service.py
│   │   └── matching_service.py
│   └── utils/               공통 유틸리티
├── templates/               Jinja2 HTML 템플릿
├── static/                  CSS, JS, 이미지
├── alembic/                 DB 마이그레이션
├── scripts/                 데이터 시드 스크립트
└── planning/                기획 원본 문서
```

---

## 배포 아키텍처

```
GitHub push (main)
    → Railway 자동 빌드 (Dockerfile / nixpacks.toml)
    → Uvicorn ASGI 서버
    → FastAPI App
    → Railway PostgreSQL
```

### 환경 변수

| 변수 | 용도 | 환경 |
|------|------|------|
| `DATABASE_URL` | PostgreSQL 연결 문자열 | 운영 |
| `SECRET_KEY` | JWT 서명 키 | 운영 |
| `ADMIN_PASSWORD` | 관리자 암호 해시 | 운영 |
| `RESEND_API_KEY` | 이메일 발송 | 운영 |
| `OPENAI_API_KEY` | AI 매칭 | 운영 |
| `GOV_DATA_API_KEY` | 공공데이터포털 API | 운영 |

개발 환경은 `.env` 파일로 관리 (`.env.example` 참조).
