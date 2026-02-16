from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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

    posts = (await db.execute(
        select(Post)
        .where(Post.is_published == True)
        .options(selectinload(Post.category))
        .order_by(Post.created_at.desc())
        .limit(12)
    )).scalars().all()

    ctx.update({"categories": categories, "posts": posts})
    return templates.TemplateResponse("index.html", ctx)
