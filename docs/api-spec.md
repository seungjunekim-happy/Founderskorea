# Founderskorea Article API 명세서

> 이 문서만으로 외부 Claude Code 에이전트가 기사 등록·관리·배치를 수행할 수 있습니다.

## Base URL

```
https://founderskorea.com/api/v1
```

## 인증

모든 API 요청에 `X-API-Key` 헤더 필수:

```
X-API-Key: your-api-key-here
```

유일한 예외: `GET /api/v1/categories` (인증 불필요)

---

## 기사 라이프사이클

```
Submit(draft) → Assign Category → Publish → [Unpublish] → [Archive]
     │                                          │
     └── Pool에서 대기 ──────────────────────────┘
```

### 상태 (status)

| 상태 | 설명 |
|------|------|
| `draft` | 초안 — Pool에 대기 중 |
| `review` | 검토 중 (예약) |
| `published` | 게시됨 — 사이트에 노출 |
| `archived` | 보관 — 비노출 |

### 카테고리 (category_slug)

| slug | 이름 |
|------|------|
| `startup` | 스타트업 |
| `gov-support` | 정부지원 |
| `investment` | 투자 |
| `know-how` | 실전노하우 |
| `networking` | 네트워킹 |

---

## 엔드포인트

### 1. 기사 등록 (Pool에 추가)

```http
POST /api/v1/articles
```

**Request Body:**

```json
{
  "title": "기사 제목 (필수, 최대 300자)",
  "summary": "기사 요약 (필수)",
  "content_md": "마크다운 본문 (필수)",
  "author": "작성자 (선택, 미입력 시 API 키 이름 사용)",
  "tag": "태그 (선택) — 뉴스, 트렌드, 분석, 리포트, 인터뷰, 칼럼, 가이드",
  "category_slug": "카테고리 (선택 — 편집자가 나중에 지정 가능)"
}
```

**Response (201):**

```json
{
  "id": 42,
  "title": "기사 제목",
  "slug": "기사-제목",
  "status": "draft",
  "source": "api",
  "category_slug": null,
  "category_name": null,
  "created_at": "2026-03-24T12:00:00Z",
  "message": "Article saved as draft"
}
```

**curl 예시:**

```bash
curl -X POST https://founderskorea.com/api/v1/articles \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "엔비디아 광통신 전략이 스타트업에 주는 시사점",
    "summary": "AI 인프라 투자 흐름 변화와 한국 스타트업 기회 분석",
    "content_md": "## 본문 시작\n\n마크다운으로 작성합니다.\n\n### 소제목\n\n- 항목 1\n- 항목 2",
    "tag": "트렌드",
    "category_slug": "startup"
  }'
```

### 2. 기사 풀 조회

```http
GET /api/v1/pool
```

**Query Parameters:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `status` | string | draft, review, published, archived |
| `category_slug` | string | 카테고리 slug 또는 `__unassigned__` (미배정) |
| `source` | string | api, seed, editor, manual |
| `q` | string | 제목 검색 |
| `page` | int | 페이지 번호 (기본 1) |
| `per_page` | int | 페이지당 항목 수 (기본 20, 최대 100) |

**Response:**

```json
{
  "items": [
    {
      "id": 42,
      "title": "기사 제목",
      "slug": "기사-제목",
      "status": "draft",
      "source": "api",
      "category_slug": "startup",
      "category_name": "스타트업",
      "created_at": "2026-03-24T12:00:00Z",
      "message": ""
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "has_next": true
}
```

**curl 예시:**

```bash
# 모든 초안 조회
curl "https://founderskorea.com/api/v1/pool?status=draft" \
  -H "X-API-Key: your-key"

# 미배정 기사만 조회
curl "https://founderskorea.com/api/v1/pool?category_slug=__unassigned__" \
  -H "X-API-Key: your-key"

# 제목 검색
curl "https://founderskorea.com/api/v1/pool?q=엔비디아" \
  -H "X-API-Key: your-key"
```

### 3. 기사 상세 조회

```http
GET /api/v1/articles/{id}
```

**Response:** 전체 기사 정보 (content_md, content_html 포함)

### 4. 기사 수정

```http
PATCH /api/v1/articles/{id}
```

변경할 필드만 전송:

```json
{
  "title": "수정된 제목",
  "content_md": "## 수정된 본문",
  "tag": "분석"
}
```

### 5. 카테고리 배정 (섹션 배치)

```http
PATCH /api/v1/articles/{id}/assign
```

```json
{
  "category_slug": "startup"
}
```

**Response:** `"message": "Assigned to 스타트업"`

### 6. 카테고리 해제

```http
DELETE /api/v1/articles/{id}/assign
```

게시 중이던 기사는 자동으로 draft 상태로 변경됩니다.

### 7. 기사 게시 (사이트 노출)

```http
POST /api/v1/articles/{id}/publish
```

카테고리가 배정되어 있어야 합니다. 미배정 시 `422` 에러.

### 8. 게시 해제

```http
POST /api/v1/articles/{id}/unpublish
```

draft 상태로 되돌립니다. 카테고리는 유지됩니다.

### 9. 기사 삭제

```http
DELETE /api/v1/articles/{id}
```

Response: `204 No Content`

### 10. 카테고리 목록 (인증 불필요)

```http
GET /api/v1/categories
```

---

## 전체 워크플로우 예시

### 시나리오: Claude Code 에이전트가 기사를 작성하여 스타트업 섹션에 게시

```bash
# Step 1: 유효한 카테고리 확인
curl https://founderskorea.com/api/v1/categories

# Step 2: 기사 등록 (Pool에 draft로 저장)
curl -X POST https://founderskorea.com/api/v1/articles \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "2026년 AI 스타트업 트렌드 분석",
    "summary": "올해 주목할 AI 스타트업 동향",
    "content_md": "## 본문...",
    "tag": "트렌드"
  }'
# → {"id": 42, "status": "draft", ...}

# Step 3: 카테고리 배정
curl -X PATCH https://founderskorea.com/api/v1/articles/42/assign \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"category_slug": "startup"}'

# Step 4: 게시
curl -X POST https://founderskorea.com/api/v1/articles/42/publish \
  -H "X-API-Key: your-key"
# → {"status": "published", "message": "Article published"}
```

### 시나리오: 기사를 다른 섹션으로 이동

```bash
# 현재 startup에 게시된 기사를 investment로 이동
curl -X POST https://founderskorea.com/api/v1/articles/42/unpublish \
  -H "X-API-Key: your-key"

curl -X PATCH https://founderskorea.com/api/v1/articles/42/assign \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"category_slug": "investment"}'

curl -X POST https://founderskorea.com/api/v1/articles/42/publish \
  -H "X-API-Key: your-key"
```

### 시나리오: 한 번에 등록 + 배치 + 게시 (원스텝)

```bash
# category_slug를 포함하여 등록하면 배정까지 한 번에 됨
curl -X POST https://founderskorea.com/api/v1/articles \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "기사 제목",
    "summary": "요약",
    "content_md": "본문",
    "category_slug": "startup"
  }'
# → {"id": 43, "status": "draft", "category_slug": "startup"}

# 바로 게시
curl -X POST https://founderskorea.com/api/v1/articles/43/publish \
  -H "X-API-Key: your-key"
```

---

## 에러 코드

| 코드 | 설명 |
|------|------|
| `400` | 잘못된 category_slug 등 유효성 오류 |
| `401` | API 키 누락 또는 유효하지 않음 |
| `404` | 기사를 찾을 수 없음 |
| `422` | 카테고리 미배정 상태에서 게시 시도 |

## 기사 풀 UI

브라우저에서 `https://founderskorea.com/pool` 접속 시 전체 기사 풀을 시각적으로 확인할 수 있습니다.
- 상태/카테고리/출처별 필터링
- 통계 대시보드 (전체/게시/초안/미배정)
