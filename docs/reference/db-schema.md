# DB 스키마

> ORM: SQLAlchemy 2.0 | 개발: SQLite | 운영: PostgreSQL (Railway)
> 원본 상세 스키마: [planning/05-tech-architecture.md](../../planning/05-tech-architecture.md#5-db-스키마-핵심)

---

## 현재 구현된 모델

### Post (`app/models/post.py`)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer PK | 고유 ID |
| title | String | 포스트 제목 |
| slug | String UNIQUE | URL 슬러그 |
| summary | Text | 요약 (목록 미리보기) |
| content | Text | 마크다운 본문 |
| category_id | FK → categories | 카테고리 |
| author_name | String | 작성자 이름 |
| author_info | String | 작성자 소개 |
| is_published | Boolean | 발행 여부 |
| is_featured | Boolean | 메인 노출 여부 |
| created_at | DateTime | 작성일 |
| updated_at | DateTime | 수정일 |

---

### Category (`app/models/category.py`)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer PK | 고유 ID |
| name | String | 카테고리명 |
| slug | String UNIQUE | URL 슬러그 |
| description | Text | 설명 |
| color | String | 브랜드 색상 코드 |

5개 고정: growth-playbook, ai-dx-lab, founders-voice, gov-support, success-cases

---

### GovSupportProgram (`app/models/gov_support.py`)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer PK | 고유 ID |
| title | String | 사업명 |
| organization | String | 주관기관 |
| apply_start | Date | 신청 시작일 |
| apply_end | Date | 신청 마감일 |
| target_industry | JSON | 대상 업종 (배열) |
| target_region | JSON | 대상 지역 (배열) |
| target_scale | String | 대상 규모 (예비/초기/성장기) |
| support_type | String | 지원 유형 (자금/교육/멘토링/공간) |
| support_amount | Integer | 지원 규모 (최대 금액, 원) |
| apply_method | String | 신청 방법 (URL) |
| source_url | String | 원본 공고 URL |
| tags | JSON | 키워드 태그 (배열) |
| status | String | 상태 (upcoming/open/closed) |
| scraped_at | DateTime | 수집 시각 |
| updated_at | DateTime | 업데이트 시각 |

---

### User (`app/models/user.py`)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer PK | 고유 ID |
| email | String UNIQUE | 이메일 |
| name | String | 이름 |
| is_active | Boolean | 활성 여부 |
| created_at | DateTime | 가입일 |

---

## Phase 1 추가 예정 모델

| 모델 | 테이블명 | 용도 |
|------|----------|------|
| Tag | `tags` | 포스트 태그 |
| PostTag | `post_tags` | 포스트-태그 M:N |
| Submission | `submissions` | Founder's Voice 투고 대기열 |
| Subscriber | `subscribers` | 뉴스레터 구독자 |
| UserProfile | `user_profiles` | 온보딩 퀴즈 결과 저장 |
| ProgramReview | `program_reviews` | 정부지원사업 파운더 리뷰 |
| ApplicationKit | `application_kits` | 신청 키트 (체크리스트) |

> 상세 스키마는 [planning/05-tech-architecture.md](../../planning/05-tech-architecture.md) 참조.
