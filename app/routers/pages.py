from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.dependencies import templates, common_context
from app.models.category import Category

router = APIRouter()


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request, db: AsyncSession = Depends(get_db)):
    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
    ctx = common_context(request)
    ctx["categories"] = categories
    return templates.TemplateResponse("about.html", ctx)
