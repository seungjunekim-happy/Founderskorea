from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import engine, Base, SessionLocal
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    import app.models  # noqa: F401 - ensure all models registered
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from app.seed import seed_initial_data
    from app.seed_gov import seed_gov_data
    async with SessionLocal() as session:
        await seed_initial_data(session)
        await seed_gov_data(session)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    from app.routers import home, category, gov_support, onboarding, pages, seo, feed
    app.include_router(home.router)
    app.include_router(gov_support.router)
    app.include_router(onboarding.router)
    app.include_router(pages.router)
    app.include_router(seo.router)
    app.include_router(feed.router)
    # Category router MUST be last due to catch-all /{category_slug} pattern
    app.include_router(category.router)

    return app
