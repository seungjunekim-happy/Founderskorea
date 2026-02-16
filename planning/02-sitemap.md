# The Founders Korea 사이트맵

## 현재 페이지 구조

```
/                       메인 페이지 (블로그 목록)
/post/{id}              포스트 상세 페이지
/about                  소개 페이지
```

## 목표 사이트맵

```
The Founders Korea
│
├── /                                  메인 페이지
│   ├── 히어로 (미디어 소개 + CTA)
│   ├── 에디터 픽 (주요 콘텐츠 하이라이트)
│   ├── 카테고리별 최신 콘텐츠 미리보기
│   └── 뉴스레터 구독 CTA
│
├── 콘텐츠 카테고리 ─────────────────────────────────────
│   │
│   ├── /growth-playbook                Growth Playbook (전문 리포트)
│   │   └── /growth-playbook/{slug}     리포트 상세
│   │
│   ├── /ai-dx-lab                      AI/DX Lab (신규)
│   │   └── /ai-dx-lab/{slug}           AI/DX 콘텐츠 상세
│   │
│   ├── /founders-voice                 Founder's Voice
│   │   ├── /founders-voice/{slug}      투고 글 상세
│   │   └── /founders-voice/submit      시민기자 투고 폼
│   │
│   ├── /gov-support                    Gov-Support Radar (정부지원 레이더)
│   │   ├── /gov-support/db             정부지원사업 DB (검색 가능한 데이터베이스)
│   │   ├── /gov-support/db/{id}        지원사업 상세
│   │   ├── /gov-support/db/{id}/reviews  프로그램별 커뮤니티 리뷰
│   │   ├── /gov-support/db/{id}/kit    신청 키트 (체크리스트, 가이드)
│   │   ├── /gov-support/weekly/{yyyy-ww}  주간 뉴스 (예: /gov-support/weekly/2026-07)
│   │   └── /gov-support/alerts         맞춤 알림 설정
│   │
│   └── /success-cases                  Success Cases
│       └── /success-cases/{slug}       케이스 스터디 상세
│
├── 사용자 참여 ─────────────────────────────────────────
│   │
│   ├── /onboarding                     AI 맞춤 추천 온보딩 퀴즈
│   └── /my-matches                     내 맞춤 추천 결과 (세션 기반)
│
├── 부가 페이지 ─────────────────────────────────────────
│   │
│   ├── /about                          소개 (센터 & 미디어)
│   ├── /newsletter                     뉴스레터 구독
│   ├── /contact                        상담 신청 (리드 폼)
│   ├── /digital-products               디지털 상품 — Phase 3 이후 (Freemium 전략)
│   ├── /tags                           태그 목록
│   ├── /tags/{tag}                     태그별 콘텐츠
│   └── /search?q={query}              통합 검색
│
├── 관리자 ──────────────────────────────────────────────
│   │
│   ├── /admin/login                    로그인
│   ├── /admin                          대시보드
│   ├── /admin/posts                    포스트 관리
│   ├── /admin/posts/new                새 포스트 작성
│   ├── /admin/posts/{id}/edit          포스트 수정
│   ├── /admin/submissions              시민기자 투고 검토
│   ├── /admin/gov-support              정부지원사업 DB 관리
│   └── /admin/subscribers              구독자 관리
│
└── 시스템 ──────────────────────────────────────────────
    ├── /feed.xml                       RSS 피드
    ├── /sitemap.xml                    사이트맵 (SEO)
    └── /robots.txt                     크롤러 설정
```

## URL 설계 원칙

1. **카테고리 중심** - 5대 카테고리가 URL 1차 경로
   - `/growth-playbook` - 전문 리포트 (기존 /insights)
   - `/ai-dx-lab` - AI/DX 실험실 (신규)
   - `/founders-voice` - 창업자 목소리
   - `/gov-support` - 정부지원 레이더 (기존 /weekly 확장)
   - `/success-cases` - 성공 케이스 (기존 /success-solution)

2. **슬러그 기반** - `/growth-playbook/2026-tax-guide` 형태로 SEO 친화적

3. **정부지원 특화 구조** - `/gov-support` 하위에 다층 구조
   - `/db` - 검색 가능한 데이터베이스
   - `/db/{id}` - 개별 지원사업 상세
   - `/weekly/{yyyy-ww}` - 주간 큐레이션
   - `/alerts` - 맞춤 알림 설정

4. **직관적** - URL만 보고 콘텐츠 유형 판별 가능

5. **확장 가능** - 디지털 상품 등 신규 비즈니스 모델 대응

6. **사용자 참여 URL** - 온보딩 퀴즈(`/onboarding`), 리뷰(`/reviews`) 등 사용자 인터랙션 중심 경로 분리
