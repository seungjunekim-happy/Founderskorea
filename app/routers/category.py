from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import templates, common_context
from app.models.category import Category
from app.models.post import Post

router = APIRouter()


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def legacy_post_redirect(post_id: int, db: AsyncSession = Depends(get_db)):
    post = (await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == post_id)
    )).scalar_one_or_none()
    if post and post.category:
        return RedirectResponse(
            url=f"/{post.category.slug}/{post.slug}",
            status_code=301,
        )
    return RedirectResponse(url="/", status_code=301)


@router.get("/{category_slug}", response_class=HTMLResponse)
async def category_list(request: Request, category_slug: str, page: int = 1, db: AsyncSession = Depends(get_db)):
    category = (await db.execute(
        select(Category).where(Category.slug == category_slug)
    )).scalar_one_or_none()

    if not category:
        ctx = common_context(request)
        categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
        ctx["categories"] = categories
        return templates.TemplateResponse("404.html", ctx, status_code=404)

    per_page = 12
    offset = (page - 1) * per_page
    posts_q = (await db.execute(
        select(Post)
        .where(Post.category_id == category.id, Post.is_published == True)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(per_page + 1)
    )).scalars().all()

    has_next = len(posts_q) > per_page
    posts = posts_q[:per_page]

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({
        "category": category,
        "categories": categories,
        "posts": posts,
        "page": page,
        "has_next": has_next,
        "has_prev": page > 1,
    })
    return templates.TemplateResponse("category/list.html", ctx)


@router.get("/{category_slug}/{post_slug}", response_class=HTMLResponse)
async def post_detail(request: Request, category_slug: str, post_slug: str, db: AsyncSession = Depends(get_db)):
    post = (await db.execute(
        select(Post)
        .options(selectinload(Post.category))
        .where(Post.slug == post_slug, Post.is_published == True)
    )).scalar_one_or_none()

    if not post or not post.category or post.category.slug != category_slug:
        ctx = common_context(request)
        categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
        ctx["categories"] = categories
        return templates.TemplateResponse("404.html", ctx, status_code=404)

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({"post": post, "category": post.category, "categories": categories})
    return templates.TemplateResponse("category/detail.html", ctx)
