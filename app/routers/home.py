from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import templates, common_context
from app.models.category import Category
from app.models.post import Post

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    ctx = common_context(request)

    categories = (await db.execute(
        select(Category).order_by(Category.sort_order)
    )).scalars().all()

    # All published posts for category grouping
    all_posts = (await db.execute(
        select(Post)
        .where(Post.is_published == True)
        .options(selectinload(Post.category))
        .order_by(Post.created_at.desc())
    )).scalars().all()

    # Featured: newest post overall
    featured = all_posts[0] if all_posts else None
    # Sub-featured: next 3
    sub_featured = all_posts[1:4] if len(all_posts) > 1 else []
    # Ticker headlines: latest 8
    ticker = all_posts[:8]

    # Group posts by category
    posts_by_cat = {}
    for cat in categories:
        posts_by_cat[cat.slug] = [p for p in all_posts if p.category and p.category.slug == cat.slug]

    ctx.update({
        "categories": categories,
        "posts": all_posts,
        "featured": featured,
        "sub_featured": sub_featured,
        "ticker": ticker,
        "posts_by_cat": posts_by_cat,
    })
    return templates.TemplateResponse("index.html", ctx)
