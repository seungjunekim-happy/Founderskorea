# 개발 로드맵

## 개요

Founderskorea v2는 **5대 카테고리 미디어 플랫폼 + 정부지원사업 DB + AI 매칭 + Freemium 모델**로 진화합니다.

**핵심 전략:**
- Phase 1: 미디어 플랫폼 + 정부지원 DB MVP + AI 매칭 + 커뮤니티 리뷰 (킬러 피처)
- Phase 2: CMS + 투고 시스템 + AI 챗봇 + 사용자 확보 집중 (Freemium)
- Phase 3: 데이터 기반 수익화 결정 + 프리미엄 서비스

## Phase 1: 미디어 플랫폼 + 정부지원 DB MVP + AI 매칭 (0~3개월)

**목표:** 5개 카테고리 미디어 사이트 + 정부지원사업 검색 DB MVP + AI 맞춤 추천 + 커뮤니티 리뷰 출시

| 작업 ID | 작업명 | 우선순위 | 예상 시간 | 설명 |
|---------|--------|----------|-----------|------|
| 1-1 | 프로젝트 구조 리팩토링 | 높음 | 4시간 | `app/` 디렉토리 모듈화 (models, routes, services, templates) |
| 1-2 | DB 도입 | 높음 | 6시간 | SQLAlchemy + Alembic, Post 모델 + GovSupportProgram 모델 |
| 1-3 | 5대 카테고리 라우트 | 높음 | 8시간 | Growth Playbook, AI/DX Lab, Founder's Voice, Gov-Support Radar, Success Cases |
| 1-4 | 정부지원사업 DB MVP | 높음 | 12시간 | 검색, 필터(카테고리/지역/기업규모), 상세보기, 공공데이터포털 API 연동 ← **킬러 피처** |
| 1-4a | AI 맞춤 추천 온보딩 퀴즈 | 높음 | 8시간 | 사용자 프로필 수집 → AI 매칭 점수 계산 |
| 1-4b | 커뮤니티 리뷰 시스템 | 높음 | 6시간 | 프로그램별 리뷰/별점/성공여부 |
| 1-4c | 신청 키트 MVP | 중간 | 4시간 | 인기 프로그램 20% 대상 체크리스트/가이드 |
| 1-5 | 메인 페이지 개편 | 높음 | 6시간 | 히어로 섹션 + 5대 카테고리 미리보기 + 정부지원 DB 검색 위젯 |
| 1-6 | 헤더/네비게이션 개편 | 높음 | 4시간 | 5대 카테고리 메뉴 구조 |
| 1-7 | 슬러그 기반 URL | 높음 | 3시간 | `/posts/{slug}` (SEO 친화적) |
| 1-8 | 마크다운 렌더링 | 높음 | 3시간 | Python-Markdown + 코드 하이라이팅 |
| 1-9 | SEO 메타 태그 | 높음 | 4시간 | Open Graph, Twitter Cards, JSON-LD, sitemap.xml, robots.txt |
| 1-10 | 카테고리별 컬러 시스템 | 중간 | 3시간 | 5색 브랜드 아이덴티티 (Growth=청록, AI=보라, Voice=주황, Gov=파랑, Success=초록) |
| 1-11 | RSS 피드 | 중간 | 2시간 | 카테고리별 RSS 제공 |
| 1-12 | 페이지네이션 | 중간 | 2시간 | 카테고리별 포스트 목록 페이지네이션 |

**산출물:** 5개 카테고리 미디어 사이트 + 정부지원사업 검색 DB MVP + AI 매칭 + 커뮤니티 리뷰

---

## Phase 2: CMS + 투고 + AI 챗봇 + 사용자 확보 (3~6개월)

**목표:** CMS + 시민기자 투고 + 정부지원 자동수집 + AI 챗봇 추천 + 사용자 확보 집중

> **Phase 2 핵심: 사용자 확보 + 데이터 수집 (Freemium 전략)**

| 작업 ID | 작업명 | 우선순위 | 예상 시간 | 설명 |
|---------|--------|----------|-----------|------|
| 2-1 | 관리자 인증 + 대시보드 | 높음 | 8시간 | Flask-Login, 관리자 대시보드 (포스트/정부지원사업/투고 관리) |
| 2-2 | 마크다운 에디터 | 높음 | 6시간 | CMS 내 마크다운 에디터 (SimpleMDE/EasyMDE) |
| 2-3 | Founder's Voice 투고 폼 | 높음 | 8시간 | 시민기자 투고 폼 + 검토 워크플로 (대기/승인/거부) |
| 2-4 | Gov-Support Radar 스크래퍼 확장 | 높음 | 12시간 | 다수 소스 자동 수집 (K-Startup, 중진공, KOTRA 등), 스케줄링 (APScheduler) |
| 2-5 | 정부지원 맞춤 알림 | 중간 | 8시간 | 사용자 관심분야 등록 → 새 공고 이메일 알림 |
| 2-6 | 주간 뉴스 큐레이션 | 중간 | 6시간 | Weekly Curation (기존 기능 유지, 편집자 픽) |
| 2-7 | AI 챗봇 추천 MVP | 중간 | 10시간 | "내 사업에 맞는 지원사업 추천해줘" 자연어 질의 |
| 2-8 | 검색 기능 | 중간 | 6시간 | 포스트 + 정부지원사업 통합 검색 (PostgreSQL Full-Text Search) |
| 2-9 | 태그 시스템 | 중간 | 4시간 | 포스트 태그 (Many-to-Many), 태그별 필터 |
| 2-10 | 뉴스레터 구독 + 발송 | 중간 | 8시간 | 이메일 수집, 뉴스레터 발송 (SendGrid/Mailgun) |
| 2-11 | PostgreSQL 전환 | 중간 | 6시간 | SQLite → PostgreSQL (Railway/Supabase) |
| 2-12 | 소셜 공유 | 낮음 | 2시간 | 트위터/링크드인/카카오톡 공유 버튼 |

**산출물:** CMS + 시민기자 + 정부지원 자동수집 + AI 챗봇 추천

---

## Phase 3: 데이터 기반 수익화 + 프리미엄 (6~12개월)

**목표:** 6개월 데이터 분석 → 최적 수익 모델 결정 + 프리미엄 서비스 론칭

| 작업 ID | 작업명 | 우선순위 | 예상 시간 | 설명 |
|---------|--------|----------|-----------|------|
| 3-1 | 상담 신청 페이지 | 높음 | 6시간 | `/contact` 폼 (수집 항목: 이름, 이메일, 회사, 관심사, 문의내용), Notion/Airtable 연동 |
| 3-2 | 수익화 결정 | 높음 | 8시간 | 6개월 데이터 분석 → 최적 모델 선택 (구독/상품/광고/제휴) |
| 3-3 | 디지털 상품 시스템 | 높음 | 16시간 | 템플릿/체크리스트 판매, 결제 연동 (토스페이먼츠/PortOne), 다운로드 관리 — Phase 2에서 이동 |
| 3-4 | Success Cases CTA 강화 | 중간 | 4시간 | 성공사례 하단 "우리도 도와드려요" CTA → 상담 신청 유도 |
| 3-5 | AI 도구 제휴/어필리에이트 | 중간 | 8시간 | AI/DX Lab 카테고리에서 AI 도구 추천 + 어필리에이트 링크 |
| 3-6 | 프리미엄 리포트/교육 | 중간 | 12시간 | 유료 콘텐츠 (심층 리포트, 온라인 강의), 결제 연동 |
| 3-7 | 뉴스레터 자동 발송 | 중간 | 6시간 | 주간 뉴스레터 자동 발송 (스케줄링) |
| 3-8 | 댓글 시스템 | 낮음 | 8시간 | Disqus 또는 자체 댓글 (커뮤니티 참여) |
| 3-9 | 시민기자 프로필 | 낮음 | 6시간 | 투고자 프로필 페이지, 기고 이력 |
| 3-10 | 라이트/다크 모드 | 낮음 | 4시간 | 테마 토글 |
| 3-11 | 분석 대시보드 | 낮음 | 8시간 | 조회수, 인기 포스트, 트래픽 소스 (Google Analytics 연동) |
| 3-12 | 프리미엄 구독 | 낮음 | 12시간 | 월 5만원 프리미엄 멤버십 (전체 리포트 접근, 1:1 상담 할인) |

**산출물:** 데이터 기반 수익화 모델 결정 + 프리미엄 서비스 론칭

---

## 마일스톤 요약

```
현재 MVP (정적 블로그)
    ↓
Phase 1 (0~3개월): 5대 카테고리 + 정부지원 DB MVP + AI 매칭 + 커뮤니티 리뷰
    ↓
Phase 2 (3~6개월): CMS + 투고 + AI 챗봇 + 사용자 확보 집중 (Freemium)
    ↓
Phase 3 (6~12개월): 데이터 기반 수익화 결정 + 프리미엄 서비스
```

## 즉시 실행 가능한 다음 단계

### 1. 프로젝트 구조 리팩토링 (작업 1-1)
```
Founderskorea/
├── app/
│   ├── __init__.py          # Flask 앱 팩토리
│   ├── models/              # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── gov_support.py
│   ├── routes/              # 라우트 블루프린트
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── growth_playbook.py
│   │   ├── ai_dx_lab.py
│   │   ├── founders_voice.py
│   │   ├── gov_support_radar.py
│   │   └── success_cases.py
│   ├── services/            # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── post_service.py
│   │   └── gov_support_service.py
│   ├── templates/           # Jinja2 템플릿
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── category/
│   │   └── gov_support/
│   └── static/              # CSS, JS, 이미지
├── migrations/              # Alembic 마이그레이션
├── config.py                # 설정
├── requirements.txt
└── run.py                   # 엔트리 포인트
```

### 2. SQLAlchemy 모델 설계 (작업 1-2)

**Post 모델:**
```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # growth_playbook, ai_dx_lab, etc.
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))
    published_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    featured_image = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
```

**GovSupportProgram 모델:**
```python
class GovSupportProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    organization = db.Column(db.String(200))  # 주관 기관
    category = db.Column(db.String(100))  # R&D, 자금지원, 수출지원 등
    target = db.Column(db.String(200))  # 예비창업자, 스타트업, 중소기업 등
    budget = db.Column(db.String(100))  # 지원 금액
    region = db.Column(db.String(100))  # 지역 제한
    deadline = db.Column(db.Date)  # 마감일
    url = db.Column(db.String(500))  # 원본 공고 링크
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

### 3. 5대 카테고리 라우트 구현 (작업 1-3)

각 카테고리별 블루프린트:
- `/growth-playbook` - 성장 전략, 실전 가이드
- `/ai-dx-lab` - AI 도구, 디지털 전환
- `/founders-voice` - 창업자 인터뷰, 시민기자 투고
- `/gov-support-radar` - 정부지원사업 DB ← 킬러 피처
- `/success-cases` - 성공 사례, 리드 퍼널

### 4. 정부지원사업 DB MVP + AI 매칭 + 커뮤니티 리뷰 (작업 1-4, 1-4a, 1-4b, 1-4c)

**기능:**
- 검색 (제목, 기관, 키워드)
- 필터 (카테고리, 지역, 대상 기업 규모, 마감일 임박)
- 상세보기 (제목, 기관, 지원내용, 예산, 마감일, 신청방법)
- 공공데이터포털 API 연동 (자동 수집)
- AI 맞춤 추천 온보딩 퀴즈 (`/onboarding` → `/my-matches`)
- 커뮤니티 리뷰/별점/성공여부 (`/gov-support/db/{id}/reviews`)
- 신청 키트: 체크리스트/가이드 (`/gov-support/db/{id}/kit`)

**UI:**
- `/gov-support-radar` 메인: 검색 바 + 필터 사이드바 + 카드 리스트 + AI 매칭 점수 배지
- `/gov-support-radar/{id}` 상세: 지원사업 상세 정보 + 리뷰 요약 + 신청 키트 배너
- `/onboarding`: 5단계 퀴즈 (업종, 사업단계, 지역, 관심분야, 기업규모)
- `/my-matches`: 매칭 점수 기반 추천 목록 (세션 기반, 로그인 불필요)

### 5. 메인 페이지 개편 (작업 1-5)

**레이아웃:**
1. 히어로 섹션: "스타트업 성장의 모든 것, Founderskorea" + CTA
2. 정부지원 DB 검색 위젯 (메인에서 바로 검색 가능)
3. 5대 카테고리 미리보기 (각 카테고리별 최신 포스트 3개)
4. 주간 뉴스 큐레이션 (편집자 픽)
5. CTA: "무료 상담 신청" / "뉴스레터 구독"

---

## 기술 스택

### 백엔드
- Python 3.11+
- Flask 3.x
- SQLAlchemy (ORM)
- Alembic (마이그레이션)
- PostgreSQL (프로덕션)
- SQLite (개발)

### 프론트엔드
- Jinja2 템플릿
- TailwindCSS 4.x
- Alpine.js (경량 인터랙션)
- HTMX (선택적, 동적 로딩)

### 배포
- Railway (현재)
- Docker
- Gunicorn + Nginx

### AI
- OpenAI/Claude API (매칭 점수 계산, 챗봇 추천)

### 외부 서비스
- 공공데이터포털 API (정부지원사업)
- SendGrid/Mailgun (뉴스레터)
- 토스페이먼츠/PortOne (결제) — Phase 3 이후, Freemium 기간에는 결제 연동 불필요
- Google Analytics (분석)

---

## 성공 지표

### Phase 1
- [ ] 5대 카테고리 페이지 오픈
- [ ] 정부지원사업 DB 100개 이상 등록
- [ ] 정부지원 DB 검색 월 500회 이상
- [ ] 온보딩 퀴즈 완료 500건
- [ ] 프로그램 리뷰 50건
- [ ] 월간 방문자 1,000명

### Phase 2
- [ ] 시민기자 투고 10건 이상
- [ ] AI 챗봇 질의 1,000건/월
- [ ] 뉴스레터 구독자 500명
- [ ] 월간 방문자 3,000명

### Phase 3
- [ ] 수익화 모델 결정 및 론칭
- [ ] 상담 신청 월 20건 이상
- [ ] 디지털 상품 월 매출 100만원
- [ ] 프리미엄 구독자 10명
- [ ] 월간 방문자 10,000명

---

**다음 액션:**
1. 작업 1-1 (프로젝트 구조 리팩토링) 착수
2. 작업 1-2 (DB 모델 설계) 완료
3. 작업 1-3 (5대 카테고리 라우트) 구현
4. 작업 1-4 (정부지원 DB MVP) 개발 ← 최우선
5. 작업 1-5 (메인 페이지 개편) 디자인