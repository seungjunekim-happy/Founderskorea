# 5대 콘텐츠 카테고리

> 원본 기획: [planning/01-site-overview.md](../../planning/01-site-overview.md#5-핵심-콘텐츠-카테고리-5개-축)
> 콘텐츠 전략 상세: [planning/07-content-strategy.md](../../planning/07-content-strategy.md)

---

## 카테고리 구조

| 우선순위 | 카테고리 | URL | 작성자 |
|----------|----------|-----|--------|
| 1 | Gov-Support Radar | `/gov-support` | 스크래퍼 + 편집 |
| 2 | Growth Playbook | `/growth-playbook` | 한국창업경영센터 전문가 |
| 3 | Success Cases | `/success-cases` | 한국창업경영센터 |
| 4 | AI/DX Lab | `/ai-dx-lab` | 센터 전문가 + 외부 전문가 |
| 5 | Founder's Voice | `/founders-voice` | 창업가 직접 투고 |

---

## 각 카테고리 상세

### 1. Gov-Support Radar (정부지원사업 레이더)
- 킬러 피처 — [별도 문서](gov-support-radar.md) 참조
- 508개+ 정부지원사업 DB + 검색/필터 + AI 매칭 + 커뮤니티 리뷰
- 발행 형태: DB 상시 업데이트 + 주간 뉴스 큐레이션 (매주 월요일)

### 2. Growth Playbook (성장 플레이북)
- 세무/법률/경영 심층 리포트, 성장 전략
- 발행 빈도: 주 1~2회 | 길이: 2,000~5,000자
- 예시: "2026년 소상공인 세무 변경사항 총정리", "프랜차이즈 창업 법률 체크리스트"

### 3. Success Cases (성공 사례)
- 한국창업경영센터 실제 컨설팅 성공 사례 (익명화)
- 발행 빈도: 월 2~4회 | 목적: 컨설팅 리드 창출
- 예시: "정부지원사업 3회 탈락 후 합격한 사업계획서의 비밀"

### 4. AI/DX Lab (AI·디지털전환 연구소)
- AI 도구 비교, 도입 가이드, 디지털전환 실전 사례
- 발행 빈도: 주 1회 | 길이: 1,500~3,000자
- 예시: "소상공인을 위한 AI 고객응대 툴 TOP 5 비교"

### 5. Founder's Voice (창업가 목소리)
- 현직 창업가 직접 투고 — 현장 운영 노하우, 실패 극복기
- 발행 빈도: 주 2~3회 (투고량에 따라)
- 투고 경로: `/founders-voice/submit` (Phase 2 구현 예정)

---

## DB 모델 매핑

```python
# Category 5개 고정 (categories 테이블)
slugs = [
    "growth-playbook",
    "ai-dx-lab",
    "founders-voice",
    "gov-support",
    "success-cases",
]
```

`Post.category_id` → `Category.id` (Foreign Key)

---

## 콘텐츠 → 리드 전환 경로

```
콘텐츠 소비
    → 온보딩 퀴즈 ("내 사업 맞춤 추천받기")
    → 뉴스레터/알림 구독  (이메일 확보)
    → "신청 도움받기" CTA
    → 상담 신청 (/contact)
    → 컨설팅 계약 (매출)
```

Success Cases 하단에는 "유사 사례 무료 상담받기" CTA 강화 배치.
