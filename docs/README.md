# The Founders Korea — 문서 인덱스

> 실전 벤처 미디어 + 정부지원사업 DB 플랫폼
> 운영 주체: 한국창업경영센터 | 프레임워크: FastAPI + Jinja2

---

## 문서 구조 (Diátaxis 기반 축소판)

| 섹션 | 경로 | 내용 |
|------|------|------|
| 개념(Concepts) | `docs/concepts/` | 아키텍처, 설계 철학 |
| 가이드(Guides) | `docs/guides/` | 개발 환경 설정, 배포 절차 |
| 참조(Reference) | `docs/reference/` | API 라우트 목록, DB 스키마 |
| 기능(Features) | `docs/features/` | 핵심 기능 명세 |

---

## 빠른 탐색

### 시작하기
- [개발 환경 설정](guides/setup.md) — Clone, venv, DB 초기화, 서버 실행
- [Railway 배포](guides/deployment.md) — 운영 환경 배포 절차

### 아키텍처
- [기술 아키텍처](concepts/architecture.md) — 스택, 앱 구조, 배포 다이어그램

### 참조
- [API 라우트 목록](reference/api-routes.md) — 전체 엔드포인트 일람
- [DB 스키마](reference/db-schema.md) — 모델 및 테이블 구조

### 기능 명세
- [Gov-Support Radar](features/gov-support-radar.md) — 정부지원사업 DB (킬러 피처)
- [온보딩 퀴즈](features/onboarding-quiz.md) — AI 매칭 퀴즈
- [5대 콘텐츠 카테고리](features/content-categories.md) — 카테고리 구조 및 전략

---

## 기획 원본 (planning/)

초기 기획 문서는 `planning/` 폴더에 원본 그대로 보존됩니다.

| 파일 | 내용 |
|------|------|
| [01-site-overview.md](../planning/01-site-overview.md) | 프로젝트 개요, 사업 배경, 핵심 타겟 |
| [02-sitemap.md](../planning/02-sitemap.md) | 사이트맵 전체 구조 |
| [03-feature-spec.md](../planning/03-feature-spec.md) | 기능 명세서 (Phase 1~3) |
| [04-design-system.md](../planning/04-design-system.md) | 디자인 시스템 |
| [05-tech-architecture.md](../planning/05-tech-architecture.md) | 기술 아키텍처 상세 |
| [06-development-roadmap.md](../planning/06-development-roadmap.md) | 개발 로드맵 |
| [07-content-strategy.md](../planning/07-content-strategy.md) | 콘텐츠 전략 |
| [08-ui-screens.md](../planning/08-ui-screens.md) | UI 화면 명세 |
| [09-business-strategy.md](../planning/09-business-strategy.md) | 비즈니스 전략 |

---

## 현재 구현 상태

- FastAPI 서버, Jinja2 렌더링 완료
- SQLAlchemy 모델 5개: Post, Category, Tag, User, GovSupportProgram
- 라우터 7개: home, category, gov_support, onboarding, pages, feed, seo
- 서비스 2개: GovSupportService, MatchingService
- Railway 배포 설정 완료 (railway.toml, Dockerfile, nixpacks.toml)
