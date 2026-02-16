from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.category import Category
from app.models.post import Post
from app.config import settings

router = APIRouter()


def _build_rss(title: str, link: str, description: str, posts: list) -> str:
    base = settings.BASE_URL
    items = []
    for post in posts:
        cat_slug = post.category.slug if post.category else "startup"
        url = f"{base}/{cat_slug}/{post.slug}"
        items.append(f"""    <item>
      <title>{post.title}</title>
      <link>{url}</link>
      <description>{post.summary or ''}</description>
      <pubDate>{post.created_at.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
      <guid>{url}</guid>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <language>ko</language>
{chr(10).join(items)}
  </channel>
</rss>"""


@router.get("/feed.xml", response_class=Response)
async def rss_feed(db: AsyncSession = Depends(get_db)):
    posts = (await db.execute(
        select(Post)
        .where(Post.is_published == True)
        .options(selectinload(Post.category))
        .order_by(Post.created_at.desc())
        .limit(20)
    )).scalars().all()

    xml = _build_rss(
        "Founderskorea",
        settings.BASE_URL,
        "창업자를 위한 인사이트와 정보",
        posts,
    )
    return Response(content=xml, media_type="application/rss+xml")


@router.get("/feed/{category_slug}.xml", response_class=Response)
async def category_rss(category_slug: str, db: AsyncSession = Depends(get_db)):
    category = (await db.execute(
        select(Category).where(Category.slug == category_slug)
    )).scalar_one_or_none()

    if not category:
        return Response(content="Not found", status_code=404)

    posts = (await db.execute(
        select(Post)
        .where(Post.is_published == True, Post.category_id == category.id)
        .options(selectinload(Post.category))
        .order_by(Post.created_at.desc())
        .limit(20)
    )).scalars().all()

    xml = _build_rss(
        f"Founderskorea - {category.name}",
        f"{settings.BASE_URL}/{category.slug}",
        category.description or "",
        posts,
    )
    return Response(content=xml, media_type="application/rss+xml")
