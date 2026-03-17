# Gov-Support Radar (정부지원사업 레이더)

> 킬러 피처 — 플랫폼 차별화 핵심
> 원본 기획: [planning/03-feature-spec.md](../../planning/03-feature-spec.md#f1-3-정부지원사업-db-mvp)

---

## 개요

508개+ 정부지원사업을 검색/필터링할 수 있는 DB 플랫폼.
bizinfo.go.kr(정부 포털) 대비 차별화: AI 매칭 + 커뮤니티 리뷰 + 신청 키트.

---

## 핵심 기능

### 1. 검색 및 필터 DB (`/gov-support/db`)

- 키워드 검색 (사업명, 주관기관, 태그)
- 필터: 지역 / 업종 / 지원유형(자금·교육·멘토링·공간·판로) / 상태(모집중·예정·마감)
- 카드형 목록: 마감일 D-day 뱃지, 지원금액, 상태 표시
- 상세 페이지: 사업명, 주관기관, 신청기간, 지원대상, 지원내용, 원문 링크

### 2. AI 맞춤 추천 (`/onboarding`)

- 온보딩 퀴즈 5문항: 업종 / 창업 단계 / 사업 규모 / 지역 / 관심 분야
- 퀴즈 결과 → `matching_service.py`로 프로그램별 적합도 점수 산출
- 결과 페이지: "내 사업 적합도 85%" 등 매칭 점수 표시

### 3. 커뮤니티 리뷰 (Phase 1 후반)

- 파운더 리뷰: 별점(1~5), 텍스트, 성공/실패/진행중 태그, 신청 팁
- 성공률 통계: 리뷰 데이터 기반 프로그램별 실제 선정율
- 모델: `ProgramReview` (program_reviews 테이블)

### 4. 신청 키트 (Phase 1 후반)

- 인기 프로그램 상위 20%에 대한 실행 가이드
- 서류 준비 체크리스트, 사업계획서 팁 (마크다운 기반)
- 모델: `ApplicationKit` (application_kits 테이블)

---

## 데이터 수집 소스

| 소스 | 방식 | 빈도 |
|------|------|------|
| K-Startup (k-startup.go.kr) | 크롤링 | 일 1회 |
| 공공데이터포털 (data.go.kr) | API | 일 1회 |
| 중소벤처기업부 (mss.go.kr) | 크롤링 | 일 1회 |
| 창업진흥원 (kised.or.kr) | 크롤링 | 일 1회 |
| 서울/경기 지자체 | 크롤링 | 주 2회 |

수집 자동화: APScheduler 일 1회 실행 (Phase 2 구현 예정).

---

## 경쟁사 대비 차별화

| 항목 | bizinfo.go.kr | K-Startup | The Founders Korea |
|------|--------------|-----------|-------------------|
| UX | 관료적 UI | 복잡한 메뉴 | 직관적 검색/필터 |
| 맞춤 추천 | 없음 | 기본 필터 | AI 매칭 점수 |
| 커뮤니티 | 없음 | 없음 | 파운더 리뷰 + 팁 |
| 실행 지원 | 없음 | 일부 교육 | 신청 키트 + 컨설팅 연결 |

---

## 구현 파일

- `app/models/gov_support.py` — GovSupportProgram 모델
- `app/routers/gov_support.py` — 라우트 (랜딩, DB 검색, 상세)
- `app/services/gov_support_service.py` — 검색/필터 로직
- `app/services/matching_service.py` — AI 매칭 점수 산출
- `app/seed_gov.py` — 샘플 데이터 시드
