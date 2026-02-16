from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.post import Post
from app.utils.slug import make_slug
from datetime import datetime, timezone

CATEGORIES = [
    {"name": "스타트업", "slug": "startup", "description": "스타트업 생태계 뉴스와 트렌드", "icon": "rocket", "color": "#3b82f6", "sort_order": 1},
    {"name": "정부지원", "slug": "gov-support", "description": "정부지원사업 정보와 신청 가이드", "icon": "building", "color": "#10b981", "sort_order": 2},
    {"name": "투자", "slug": "investment", "description": "투자 유치 전략과 VC 소식", "icon": "chart", "color": "#f59e0b", "sort_order": 3},
    {"name": "실전노하우", "slug": "know-how", "description": "창업 실전 경험과 노하우 공유", "icon": "lightbulb", "color": "#8b5cf6", "sort_order": 4},
    {"name": "네트워킹", "slug": "networking", "description": "창업자 커뮤니티와 이벤트", "icon": "people", "color": "#ef4444", "sort_order": 5},
]

INITIAL_POSTS = [
    {
        "title": "Founderskorea에 오신 것을 환영합니다",
        "summary": "창업자들을 위한 커뮤니티, Founderskorea의 첫 번째 이야기입니다.",
        "content_md": """안녕하세요! Founderskorea에 오신 것을 환영합니다.

우리는 한국의 창업자들이 서로 연결되고, 배우고, 성장할 수 있는 플랫폼을 만들고 있습니다.

이 블로그에서는 스타트업 생태계의 최신 소식, 창업 노하우, 그리고 성공 사례들을 공유할 예정입니다.

함께 성장해 나가요!""",
        "author": "Founderskorea Team",
        "tag": "공지",
        "category_slug": "startup",
        "date": "2026-02-17",
    },
    {
        "title": "2026년 스타트업 트렌드 전망",
        "summary": "올해 주목해야 할 스타트업 트렌드와 기회를 살펴봅니다.",
        "content_md": """2026년은 AI와 자동화가 더욱 깊숙이 우리 생활에 들어오는 해가 될 것입니다.

## 주요 트렌드

- **AI 에이전트** - 단순 챗봇을 넘어 실제 업무를 수행하는 AI
- **기후테크** - 탄소 중립을 위한 기술 솔루션
- **헬스케어 AI** - 개인 맞춤형 건강 관리
- **크리에이터 이코노미** - 1인 창업의 새로운 물결

이 트렌드들을 잘 파악하고 준비하는 창업자가 성공할 것입니다.""",
        "author": "Founderskorea Team",
        "tag": "트렌드",
        "category_slug": "startup",
        "date": "2026-02-15",
    },
    {
        "title": "초기 스타트업을 위한 MVP 전략",
        "summary": "최소 기능 제품(MVP)을 효과적으로 만드는 방법을 알아봅니다.",
        "content_md": """MVP(Minimum Viable Product)는 스타트업의 첫 걸음입니다.

## MVP 성공 원칙

1. **핵심 가치에 집중** - 하나의 문제를 완벽하게 해결하세요
2. **빠르게 출시** - 완벽함보다 속도가 중요합니다
3. **사용자 피드백** - 데이터 기반으로 개선하세요
4. **반복 개선** - 작은 개선을 빠르게 반복하세요

기억하세요: 완벽한 제품보다 빠른 학습이 더 중요합니다.""",
        "author": "Founderskorea Team",
        "tag": "전략",
        "category_slug": "know-how",
        "date": "2026-02-10",
    },
]


async def seed_initial_data(session: AsyncSession):
    result = await session.execute(select(Category).limit(1))
    if result.scalar_one_or_none():
        return

    from app.utils.markdown import render_markdown

    cat_map = {}
    for cat_data in CATEGORIES:
        cat = Category(**cat_data)
        session.add(cat)
        cat_map[cat_data["slug"]] = cat

    await session.flush()

    for post_data in INITIAL_POSTS:
        cat_slug = post_data.pop("category_slug")
        date_str = post_data.pop("date")
        cat = cat_map[cat_slug]
        post = Post(
            title=post_data["title"],
            slug=make_slug(post_data["title"]),
            summary=post_data["summary"],
            content_md=post_data["content_md"],
            content_html=render_markdown(post_data["content_md"]),
            author=post_data["author"],
            tag=post_data["tag"],
            category_id=cat.id,
            created_at=datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc),
            updated_at=datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc),
        )
        session.add(post)

    await session.commit()
