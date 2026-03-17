# Railway 배포

---

## 배포 방식

GitHub `main` 브랜치 push → Railway 자동 빌드 및 배포

---

## 배포 설정 파일

| 파일 | 역할 |
|------|------|
| `railway.toml` | Railway 서비스 설정 (start 커맨드 등) |
| `Dockerfile` | 컨테이너 빌드 명세 |
| `nixpacks.toml` | nixpacks 빌드 설정 |
| `Procfile` | 프로세스 선언 (`web: uvicorn main:app ...`) |
| `runtime.txt` | Python 버전 고정 |

---

## 환경 변수 설정 (Railway 대시보드)

Railway 프로젝트 → Variables 탭에서 설정:

```
DATABASE_URL         PostgreSQL 연결 문자열 (Railway가 자동 제공)
SECRET_KEY           랜덤 생성 문자열 (32자+)
ADMIN_PASSWORD       관리자 비밀번호 해시
RESEND_API_KEY       이메일 발송 (Resend 서비스)
OPENAI_API_KEY       AI 매칭 기능
GOV_DATA_API_KEY     공공데이터포털 API
BASE_URL             https://founderskorea.com (운영 도메인)
```

---

## 배포 절차

```bash
# 1. 로컬 테스트
uvicorn main:app --reload

# 2. Alembic 마이그레이션 파일 생성 (스키마 변경 시)
alembic revision --autogenerate -m "변경 내용 설명"

# 3. main 브랜치에 push → Railway 자동 배포
git add .
git commit -m "feat: 기능 설명"
git push origin main
```

Railway가 Dockerfile 또는 nixpacks로 빌드 후 자동 재시작합니다.

---

## 운영 DB 마이그레이션

Railway 콘솔에서 직접 실행:

```bash
railway run alembic upgrade head
```

또는 `Procfile`에 마이그레이션 커맨드를 release 단계에 추가합니다.

---

## 주의사항

- `railway.toml`, `Dockerfile`, `nixpacks.toml` 절대 삭제 금지
- 운영 DB는 Railway PostgreSQL 사용 (`DATABASE_URL` 자동 주입)
- 로컬 개발은 SQLite (`sqlite+aiosqlite:///./founderskorea.db`)
