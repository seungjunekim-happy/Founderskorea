from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db
from app.models.post import Post
from app.models.category import Category
from app.auth import verify_api_key
from app.utils.slug import make_slug
from app.utils.markdown import render_markdown
from app.schemas.article import (
    ArticleCreate, ArticleUpdate, ArticleAssign,
    ArticleResponse, ArticleDetail, ArticleListResponse,
    CategoryResponse,
)

router = APIRouter(prefix="/api/v1", tags=["api"])


def _make_unique_slug(title: str, existing_slugs: list[str]) -> str:
    """Generate unique slug, appending -2, -3 etc if needed."""
    base = make_slug(title)
    slug = base
    counter = 2
    while slug in existing_slugs:
        slug = f"{base}-{counter}"
        counter += 1
    return slug


def _post_to_response(post: Post, message: str = "") -> ArticleResponse:
    return ArticleResponse(
        id=post.id,
        title=post.title,
        slug=post.slug,
        status=post.status,
        source=post.source,
        category_slug=post.category.slug if post.category else None,
        category_name=post.category.name if post.category else None,
        created_at=post.created_at,
        message=message,
    )


def _post_to_detail(post: Post) -> ArticleDetail:
    return ArticleDetail(
        id=post.id,
        title=post.title,
        slug=post.slug,
        summary=post.summary,
        content_md=post.content_md,
        content_html=post.content_html,
        author=post.author,
        tag=post.tag,
        status=post.status,
        source=post.source,
        api_key_name=post.api_key_name,
        category_slug=post.category.slug if post.category else None,
        category_name=post.category.name if post.category else None,
        created_at=post.created_at,
        updated_at=post.updated_at,
        published_at=post.published_at,
    )


# ──────────────────────────────────────
# Categories (public, no auth needed for listing)
# ──────────────────────────────────────

@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).order_by(Category.sort_order))
    return result.scalars().all()


# ──────────────────────────────────────
# Article Pool
# ──────────────────────────────────────

@router.get("/pool", response_model=ArticleListResponse)
async def list_pool(
    status: Optional[str] = None,
    category_slug: Optional[str] = None,
    source: Optional[str] = None,
    q: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    query = select(Post).options(selectinload(Post.category))
    count_query = select(func.count(Post.id))

    # Apply filters
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

    # Count
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Paginate
    query = query.order_by(Post.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    posts = result.scalars().all()

    return ArticleListResponse(
        items=[_post_to_response(p) for p in posts],
        total=total,
        page=page,
        per_page=per_page,
        has_next=(page * per_page < total),
    )


# ──────────────────────────────────────
# Article CRUD
# ──────────────────────────────────────

@router.post("/articles", response_model=ArticleResponse, status_code=201)
async def create_article(
    body: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    # Resolve category if provided
    category = None
    if body.category_slug:
        result = await db.execute(select(Category).where(Category.slug == body.category_slug))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(400, f"Invalid category_slug: {body.category_slug}")

    # Generate unique slug
    existing = await db.execute(select(Post.slug))
    existing_slugs = [r[0] for r in existing.all()]
    slug = _make_unique_slug(body.title, existing_slugs)

    now = datetime.now(timezone.utc)
    post = Post(
        title=body.title,
        slug=slug,
        summary=body.summary,
        content_md=body.content_md,
        content_html=render_markdown(body.content_md),
        author=body.author or key_name,
        tag=body.tag,
        status="draft",
        source="api",
        api_key_name=key_name,
        category_id=category.id if category else None,
        created_at=now,
        updated_at=now,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post, attribute_names=["category"])

    return _post_to_response(post, message="Article saved as draft")


@router.get("/articles/{article_id}", response_model=ArticleDetail)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")
    return _post_to_detail(post)


@router.patch("/articles/{article_id}", response_model=ArticleDetail)
async def update_article(
    article_id: int,
    body: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")

    if body.title is not None:
        post.title = body.title
        # Regenerate slug
        existing = await db.execute(select(Post.slug).where(Post.id != article_id))
        existing_slugs = [r[0] for r in existing.all()]
        post.slug = _make_unique_slug(body.title, existing_slugs)
    if body.summary is not None:
        post.summary = body.summary
    if body.content_md is not None:
        post.content_md = body.content_md
        post.content_html = render_markdown(body.content_md)
    if body.author is not None:
        post.author = body.author
    if body.tag is not None:
        post.tag = body.tag
    if body.category_slug is not None:
        cat_result = await db.execute(select(Category).where(Category.slug == body.category_slug))
        cat = cat_result.scalar_one_or_none()
        if not cat:
            raise HTTPException(400, f"Invalid category_slug: {body.category_slug}")
        post.category_id = cat.id

    post.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(post, attribute_names=["category"])
    return _post_to_detail(post)


# ──────────────────────────────────────
# Assign / Unassign Category
# ──────────────────────────────────────

@router.patch("/articles/{article_id}/assign", response_model=ArticleResponse)
async def assign_category(
    article_id: int,
    body: ArticleAssign,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")

    cat_result = await db.execute(select(Category).where(Category.slug == body.category_slug))
    cat = cat_result.scalar_one_or_none()
    if not cat:
        raise HTTPException(400, f"Invalid category_slug: {body.category_slug}")

    post.category_id = cat.id
    post.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(post, attribute_names=["category"])
    return _post_to_response(post, message=f"Assigned to {cat.name}")


@router.delete("/articles/{article_id}/assign", response_model=ArticleResponse)
async def unassign_category(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")

    post.category_id = None
    if post.status == "published":
        post.status = "draft"
        post.published_at = None
    post.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(post, attribute_names=["category"])
    return _post_to_response(post, message="Category unassigned, reverted to draft")


# ──────────────────────────────────────
# Publish / Unpublish
# ──────────────────────────────────────

@router.post("/articles/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")
    if not post.category_id:
        raise HTTPException(422, "Cannot publish without a category. Assign a category first.")

    now = datetime.now(timezone.utc)
    post.status = "published"
    post.published_at = now
    post.updated_at = now
    await db.commit()
    await db.refresh(post, attribute_names=["category"])
    return _post_to_response(post, message="Article published")


@router.post("/articles/{article_id}/unpublish", response_model=ArticleResponse)
async def unpublish_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(
        select(Post).options(selectinload(Post.category)).where(Post.id == article_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")

    post.status = "draft"
    post.published_at = None
    post.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(post, attribute_names=["category"])
    return _post_to_response(post, message="Article unpublished")


# ──────────────────────────────────────
# Delete
# ──────────────────────────────────────

@router.delete("/articles/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    key_name: str = Depends(verify_api_key),
):
    result = await db.execute(select(Post).where(Post.id == article_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Article not found")
    await db.delete(post)
    await db.commit()
