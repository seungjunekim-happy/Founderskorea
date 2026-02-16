from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.dependencies import templates, common_context
from app.models.category import Category
from app.models.user import UserProfile
from app.models.gov_support import GovSupportProgram
from app.services.matching_service import calculate_matches

import uuid

router = APIRouter()


@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding(request: Request, db: AsyncSession = Depends(get_db)):
    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
    ctx = common_context(request)
    ctx["categories"] = categories
    return templates.TemplateResponse("onboarding/quiz.html", ctx)


@router.post("/onboarding", response_class=HTMLResponse)
async def submit_onboarding(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()

    session_id = str(uuid.uuid4())

    profile = UserProfile(
        session_id=session_id,
        industry=form.get("industry", ""),
        business_stage=form.get("business_stage", ""),
        business_size=form.get("business_size", ""),
        region=form.get("region", ""),
        interests=form.get("interests", ""),
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    programs = (await db.execute(
        select(GovSupportProgram).where(GovSupportProgram.is_active == True)
    )).scalars().all()

    matches = calculate_matches(profile, programs)

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({
        "categories": categories,
        "matches": matches,
        "profile": profile,
        "session_id": session_id,
    })
    return templates.TemplateResponse("onboarding/results.html", ctx)


@router.get("/my-matches/{session_id}", response_class=HTMLResponse)
async def my_matches(request: Request, session_id: str, db: AsyncSession = Depends(get_db)):
    profile = (await db.execute(
        select(UserProfile).where(UserProfile.session_id == session_id)
    )).scalar_one_or_none()

    if not profile:
        ctx = common_context(request)
        categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
        ctx["categories"] = categories
        return templates.TemplateResponse("404.html", ctx, status_code=404)

    programs = (await db.execute(
        select(GovSupportProgram).where(GovSupportProgram.is_active == True)
    )).scalars().all()

    matches = calculate_matches(profile, programs)

    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()

    ctx = common_context(request)
    ctx.update({
        "categories": categories,
        "matches": matches,
        "profile": profile,
        "session_id": session_id,
    })
    return templates.TemplateResponse("onboarding/results.html", ctx)
