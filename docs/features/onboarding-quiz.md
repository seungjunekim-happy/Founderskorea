# 온보딩 퀴즈 (AI 매칭)

> 원본 기획: [planning/03-feature-spec.md](../../planning/03-feature-spec.md#f1-3a-ai-맞춤-추천-온보딩-퀴즈)

---

## 개요

사용자 프로필(업종/단계/규모/지역/관심분야)을 수집하여 정부지원사업 AI 매칭 점수를 산출.
bizinfo.go.kr 단순 검색 대비 핵심 차별화 포인트.

---

## 사용자 흐름

```
메인 페이지 "내 사업 맞춤 추천받기" CTA
    → /onboarding (퀴즈 5문항)
    → POST /onboarding/submit
    → /onboarding/result (매칭 결과)
    → 이메일 알림 구독 CTA
    → 상담 신청 CTA
```

---

## 퀴즈 문항 (5개)

| 순서 | 항목 | 선택지 예시 |
|------|------|-----------|
| 1 | 업종 | IT/SaaS, 제조, 음식/F&B, 유통, 서비스업, 기타 |
| 2 | 창업 단계 | 예비창업, 초기(1년 미만), 성장기(1~3년), 성숙기(3년+) |
| 3 | 사업 규모 | 1인, 5인 이하, 10인 이하, 50인 이하, 50인+ |
| 4 | 지역 | 서울, 경기, 부산, 대구, 인천, 기타 |
| 5 | 관심 분야 | 자금지원, R&D, 교육/멘토링, 공간지원, 판로개척 (복수 선택) |

---

## 매칭 로직 (`app/services/matching_service.py`)

사용자 프로필과 `gov_support_programs` 각 항목을 비교하여 적합도 점수(0~100) 산출:

- `target_industry` 일치 여부 → 가중치 30%
- `target_region` 일치 여부 → 가중치 20%
- `target_scale` 일치 여부 → 가중치 20%
- 관심 분야 vs `support_type` 일치 → 가중치 30%

결과: 상위 매칭 프로그램 10개 반환 (점수 내림차순).

---

## 데이터 저장

퀴즈 완료 시 `user_profiles` 테이블에 저장 (비회원: session_id 기반):

| 컬럼 | 값 |
|------|-----|
| session_id | 쿠키 세션 ID |
| industry | 선택 업종 |
| business_stage | 창업 단계 |
| business_scale | 사업 규모 |
| region | 지역 |
| interests | 관심 분야 JSON 배열 |

재방문 시 세션으로 프로필 불러와 자동 추천 제공.

---

## 구현 파일

- `app/routers/onboarding.py` — GET /onboarding, POST /onboarding/submit, GET /onboarding/result
- `app/services/matching_service.py` — 매칭 점수 산출 로직
- `templates/onboarding/` — 퀴즈 + 결과 템플릿 (Phase 1 구현 예정)
