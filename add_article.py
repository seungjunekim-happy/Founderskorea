"""
One-time script to insert the Nvidia/Palantir/AI Infrastructure article
into the existing SQLite database.

Usage:
    python add_article.py
"""
import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.models.category import Category
from app.models.post import Post
from app.utils.slug import make_slug
from app.utils.markdown import render_markdown

TITLE = "엔비디아·팔란티어·AI 인프라 — 2026년 스타트업이 주목해야 할 AI 투자 시그널"

SUMMARY = (
    "글로벌 AI 투자 흐름이 반도체에서 에이전트·인프라로 빠르게 이동하고 있습니다. "
    "엔비디아의 광통신 투자, 팔란티어의 에이전트 AI 전략이 한국 스타트업 생태계에 던지는 시사점을 분석합니다."
)

CONTENT_MD = """## AI 투자 지형이 바뀌고 있다

2026년 1분기, 글로벌 AI 시장은 뚜렷한 전환점을 맞이하고 있습니다. 미국 주식시장 전문 분석가 올랜도 킴의 최근 분석에 따르면, **"AI 한다고 다 오르는 시대는 끝났다"**는 메시지가 시장 전반에 퍼지고 있습니다. 이는 단순한 주식 이야기가 아닙니다. 스타트업 창업자들이 반드시 읽어야 할 **기술 투자 방향의 전환 신호**입니다.

## 핵심 트렌드 3가지

### 1. 엔비디아 — GPU를 넘어 '빛'에 투자하다

엔비디아가 광통신(Photonics) 기술에 대규모 투자를 단행했습니다. 이는 AI 데이터센터의 병목이 **연산 능력에서 데이터 전송 속도**로 이동하고 있음을 의미합니다.

**스타트업 시사점:**
- AI 인프라 스타트업에 새로운 기회 창출 — 광통신 기반 네트워킹, 저지연 데이터 파이프라인
- GPU 의존도를 낮추는 **경량화·최적화 기술**이 차별화 포인트
- 엣지 AI, 온디바이스 AI 스타트업의 가치 재평가 가능성

### 2. 팔란티어 — 에이전트 AI가 밸류에이션을 결정한다

팔란티어는 높은 밸류에이션에도 불구하고 **에이전트 AI 플랫폼** 전략으로 시장의 기대를 유지하고 있습니다. "새로운 운영체계(OS)를 만드는 회사"라는 평가는 단순 SaaS를 넘어 **AI 네이티브 엔터프라이즈 인프라**로 진화하고 있음을 보여줍니다.

**스타트업 시사점:**
- B2B AI 스타트업은 단순 도구가 아닌 **워크플로우 자체를 재설계**하는 방향으로 피벗 필요
- 에이전트 AI의 핵심은 자율 실행이 아니라 **의사결정 지원 + 실행 자동화**의 결합
- 한국 대기업의 DX 수요와 맞물려 국내 에이전트 AI B2B 시장 급성장 전망

### 3. AI 인프라 — '수도관'을 쥔 자가 승리한다

올랜도 킴은 "AI의 수도관을 쥔 기업이 대장주 중 가성비가 가장 좋다"고 분석했습니다. 이는 모델 개발보다 **AI 인프라 레이어**(데이터센터, 클라우드, 네트워킹, 보안)가 더 안정적인 수익 기반이라는 의미입니다.

**스타트업 시사점:**
- AI 모델 자체보다 **AI Ops, MLOps, 데이터 파이프라인** 스타트업이 장기적으로 유리
- 국내 AI 데이터센터 투자 확대(2026년 약 2조 원 규모)에 따른 연관 서비스 수요 폭발
- 보안·규제 대응 솔루션(AI 거버넌스, 모델 감사)이 새로운 블루오션

## AI가 시장을 잠식하나? — 창업자가 알아야 할 현실

"AI가 모든 사업 분야를 점령하는가"라는 질문에 대해 올랜도 킴은 **차별화된 시각**을 제시합니다. AI 기술 자체보다 **AI를 활용해 실제 문제를 해결하는 기업**이 최종 승자가 될 것이라는 분석입니다.

한국 스타트업에게 이는 명확한 메시지입니다:

> **"AI 기술을 만드는 회사"보다 "AI로 산업의 비효율을 해결하는 회사"가 되어라.**

## 한국 스타트업 생태계에 주는 교훈

| 글로벌 시그널 | 한국 스타트업 기회 |
|---|---|
| 엔비디아 광통신 투자 | AI 인프라 최적화·경량화 기술 |
| 팔란티어 에이전트 OS | B2B 워크플로우 자동화 플랫폼 |
| AI 인프라 밸류 상승 | MLOps·데이터 파이프라인 서비스 |
| AI 차별화 시대 진입 | 산업 특화 버티컬 AI 솔루션 |

2026년은 AI 스타트업의 **옥석 가리기**가 본격화되는 해입니다. 단순히 "AI를 사용한다"는 것만으로는 투자 유치도, 고객 확보도 어려워질 것입니다. 글로벌 투자 시그널을 읽고, **자사만의 해자(moat)**를 구축하는 것이 그 어느 때보다 중요합니다."""

AUTHOR = "Founderskorea 편집팀"
TAG = "트렌드"
CATEGORY_SLUG = "startup"
DATE_STR = "2026-03-24"


async def main() -> None:
    async with SessionLocal() as session:
        # Check for duplicate
        existing = await session.execute(
            select(Post).where(Post.title == TITLE)
        )
        if existing.scalar_one_or_none():
            print(f"[skip] Post already exists: {TITLE}")
            return

        # Resolve category
        result = await session.execute(
            select(Category).where(Category.slug == CATEGORY_SLUG)
        )
        category = result.scalar_one_or_none()
        if category is None:
            print(f"[error] Category not found: {CATEGORY_SLUG}")
            return

        created_at = datetime.fromisoformat(DATE_STR).replace(tzinfo=timezone.utc)

        post = Post(
            title=TITLE,
            slug=make_slug(TITLE),
            summary=SUMMARY,
            content_md=CONTENT_MD,
            content_html=render_markdown(CONTENT_MD),
            author=AUTHOR,
            tag=TAG,
            category_id=category.id,
            created_at=created_at,
            updated_at=created_at,
        )
        session.add(post)
        await session.commit()

        print(f"[ok] Inserted post: {TITLE}")
        print(f"     slug        : {post.slug}")
        print(f"     category_id : {category.id} ({category.name})")
        print(f"     created_at  : {post.created_at}")


if __name__ == "__main__":
    asyncio.run(main())
