from fastapi import APIRouter, Request, Query
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional

from app.dependencies import templates
from app.database import SessionLocal
from app.models.post import Post
from app.models.category import Category

router = APIRouter()


@router.get("/pool")
async def article_pool(
    request: Request,
    status: Optional[str] = None,
    category_slug: Optional[str] = None,
    source: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(1, ge=1),
):
    per_page = 50
    async with SessionLocal() as session:
        # Base queries
        query = select(Post).options(selectinload(Post.category))
        count_query = select(func.count(Post.id))

        # Filters
        if status:
            query = query.where(Post.status == status)
            count_query = count_query.where(Post.status == status)
        if category_slug == "__unassigned__":
            query = query.where(Post.category_id.is_(None))
            count_query = count_query.where(Post.category_id.is_(None))
        elif category_slug:
            cat_sub = select(Category.id).where(Category.slug == category_slug).scalar_subquery()
            query = query.where(Post.category_id == cat_sub)
            count_query = count_query.where(Post.category_id == cat_sub)
        if source:
            query = query.where(Post.source == source)
            count_query = count_query.where(Post.source == source)
        if q:
            query = query.where(Post.title.ilike(f"%{q}%"))
            count_query = count_query.where(Post.title.ilike(f"%{q}%"))

        # Total count
        total = (await session.execute(count_query)).scalar()

        # Stats
        stats_published = (await session.execute(
            select(func.count(Post.id)).where(Post.status == "published")
        )).scalar()
        stats_draft = (await session.execute(
            select(func.count(Post.id)).where(Post.status == "draft")
        )).scalar()
        stats_unassigned = (await session.execute(
            select(func.count(Post.id)).where(Post.category_id.is_(None))
        )).scalar()
        stats_total = (await session.execute(select(func.count(Post.id)))).scalar()

        # Paginate
        query = query.order_by(Post.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        posts = (await session.execute(query)).scalars().all()

        # Categories for filter dropdown
        categories = (await session.execute(
            select(Category).order_by(Category.sort_order)
        )).scalars().all()

    total_pages = (total + per_page - 1) // per_page

    return templates.TemplateResponse("pool.html", {
        "request": request,
        "posts": posts,
        "categories": categories,
        "total": total,
        "page": page,
        "total_pages": total_pages,
        "per_page": per_page,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        # Current filters (for form defaults)
        "current_status": status or "",
        "current_category": category_slug or "",
        "current_source": source or "",
        "current_q": q or "",
        # Stats
        "stats_total": stats_total,
        "stats_published": stats_published,
        "stats_draft": stats_draft,
        "stats_unassigned": stats_unassigned,
    })
