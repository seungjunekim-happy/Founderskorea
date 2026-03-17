# 개발 환경 설정

---

## 사전 요구사항

- Python 3.11+
- Git

---

## 1. 저장소 클론 및 가상환경

```bash
git clone https://github.com/your-org/founderskorea.git
cd founderskorea

python -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows
```

---

## 2. 의존성 설치

```bash
pip install -r requirements.txt
```

주요 패키지: FastAPI 0.115.6, SQLAlchemy 2.0, Alembic 1.14.1, Jinja2 3.1.5

---

## 3. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 필수 항목:

```env
DATABASE_URL=sqlite+aiosqlite:///./founderskorea.db   # 개발용 SQLite
SECRET_KEY=your-secret-key-here
BASE_URL=http://localhost:8000
```

---

## 4. DB 초기화 및 시드 데이터

```bash
# Alembic 마이그레이션 적용
alembic upgrade head

# 기본 카테고리 + 샘플 포스트 시드
python app/seed.py

# 정부지원사업 샘플 데이터 시드
python app/seed_gov.py
```

---

## 5. 개발 서버 실행

```bash
uvicorn main:app --reload --port 8000
```

브라우저에서 `http://localhost:8000` 접속.

---

## 6. 자주 쓰는 명령어

| 명령어 | 용도 |
|--------|------|
| `alembic revision --autogenerate -m "설명"` | 마이그레이션 파일 생성 |
| `alembic upgrade head` | 마이그레이션 적용 |
| `alembic downgrade -1` | 마이그레이션 롤백 |
| `python app/seed.py` | 포스트/카테고리 시드 |
| `python app/seed_gov.py` | 정부지원사업 시드 |
