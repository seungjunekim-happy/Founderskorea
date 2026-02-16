from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies import templates, common_context
from app.models.category import Category
from app.models.gov_support import GovSupportProgram, ProgramReview, ApplicationKit

router = APIRouter(prefix="/gov-support")


@router.get("/db", response_class=HTMLResponse)
async def gov_support_list(
    request: Request,
    q: str = "",
    region: str = "",
    industry: str = "",
    support_type: str = "",
    status: str = "",
    page: int = 1,
    db: AsyncSession = Depends(get_db),
):
    query = select(GovSupportProgram).where(GovSupportProgram.is_active == True)

    if q:
        query = query.where(or_(
            GovSupportProgram.title.ilike(f"%{q}%"),
            GovSupportProgram.organization.ilike(f"%{q}%"),
            GovSupportProgram.keywords.ilike(f"%{q}%"),
        ))
    if region:
        query = query.where(GovSupportProgram.region == region)
    if industry:
        query = query.where(GovSupportProgram.industry.ilike(f"%{industry}%"))
    if support_type:
        query = query.where(GovSupportProgram.support_type == support_type)
    if status:
        query = query.where(GovSupportProgram.status == status)

    per_page = 12
    offset = (page - 1) * per_page
    programs = (await db.execute(
        query.order_by(GovSupportProgram.deadline.asc().nullslast())
        .offset(offset)
        .limit(per_page + 1)
    )).scalars().all()

    has_next = len(programs) > per_page
    programs = programs[:per_page]

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({
        "programs": programs,
        "categories": categories,
        "q": q, "region": region, "industry": industry,
        "support_type": support_type, "status": status,
        "page": page, "has_next": has_next, "has_prev": page > 1,
    })

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("gov_support/_program_list.html", ctx)
    return templates.TemplateResponse("gov_support/search.html", ctx)


@router.get("/db/{program_id}", response_class=HTMLResponse)
async def gov_support_detail(request: Request, program_id: int, db: AsyncSession = Depends(get_db)):
    program = (await db.execute(
        select(GovSupportProgram)
        .options(
            selectinload(GovSupportProgram.reviews),
            selectinload(GovSupportProgram.application_kit),
        )
        .where(GovSupportProgram.id == program_id)
    )).scalar_one_or_none()

    if not program:
        ctx = common_context(request)
        categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
        ctx["categories"] = categories
        return templates.TemplateResponse("404.html", ctx, status_code=404)

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({"program": program, "categories": categories})
    return templates.TemplateResponse("gov_support/detail.html", ctx)


@router.post("/db/{program_id}/review", response_class=HTMLResponse)
async def submit_review(
    request: Request,
    program_id: int,
    db: AsyncSession = Depends(get_db),
):
    form = await request.form()
    review = ProgramReview(
        program_id=program_id,
        nickname=form.get("nickname", "익명"),
        rating=int(form.get("rating", 3)),
        content=form.get("content", ""),
        success_tag=form.get("success_tag", ""),
        tip=form.get("tip", ""),
    )
    session = db
    session.add(review)
    await session.commit()

    program = (await db.execute(
        select(GovSupportProgram)
        .options(selectinload(GovSupportProgram.reviews))
        .where(GovSupportProgram.id == program_id)
    )).scalar_one_or_none()

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
    ctx = common_context(request)
    ctx.update({"program": program, "categories": categories})

    if request.headers.get("HX-Request"):
        return templates.TemplateResponse("gov_support/_reviews.html", ctx)
    return templates.TemplateResponse("gov_support/detail.html", ctx)
