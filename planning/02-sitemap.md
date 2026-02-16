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
│   ├── /insights                      The Insights
│   │   └── /insights/{slug}           전문 리포트 상세
│   │
│   ├── /founders-voice                Founder's Voice
│   │   ├── /founders-voice/{slug}     투고 글 상세
│   │   └── /founders-voice/submit     시민기자 투고 폼
│   │
│   ├── /weekly                        Weekly Curation
│   │   └── /weekly/{yyyy-ww}          주간 뉴스 상세 (예: /weekly/2026-07)
│   │
│   └── /success-solution              Success Solution
│       └── /success-solution/{slug}   케이스 스터디 상세
│
├── 부가 페이지 ─────────────────────────────────────────
│   │
│   ├── /about                         소개 (센터 & 미디어)
│   ├── /newsletter                    뉴스레터 구독
│   ├── /contact                       상담 신청 (리드 폼)
│   ├── /tags                          태그 목록
│   ├── /tags/{tag}                    태그별 콘텐츠
│   └── /search?q={query}             통합 검색
│
├── 관리자 ──────────────────────────────────────────────
│   │
│   ├── /admin/login                   로그인
│   ├── /admin                         대시보드
│   ├── /admin/posts                   포스트 관리
│   ├── /admin/posts/new               새 포스트 작성
│   ├── /admin/posts/{id}/edit         포스트 수정
│   ├── /admin/submissions             시민기자 투고 검토
│   ├── /admin/weekly                  주간 큐레이션 관리
│   └── /admin/subscribers             구독자 관리
│
└── 시스템 ──────────────────────────────────────────────
    ├── /feed.xml                      RSS 피드
    ├── /sitemap.xml                   사이트맵 (SEO)
    └── /robots.txt                    크롤러 설정
```

## URL 설계 원칙

1. **카테고리 중심** - 4대 카테고리가 URL 1차 경로
2. **슬러그 기반** - `/insights/2026-tax-guide` 형태로 SEO 친화적
3. **주간 큐레이션** - 연도-주차 형식 (`/weekly/2026-07`)
4. **직관적** - URL만 보고 콘텐츠 유형 판별 가능
