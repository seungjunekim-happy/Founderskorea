from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.category import Category
from app.models.post import Post
from app.config import settings

router = APIRouter()


@router.get("/sitemap.xml", response_class=Response)
async def sitemap(db: AsyncSession = Depends(get_db)):
    base = settings.BASE_URL
    categories = (await db.execute(select(Category).order_by(Category.sort_order))).scalars().all()
    posts = (await db.execute(
        select(Post).where(Post.is_published == True).order_by(Post.created_at.desc())
    )).scalars().all()

    urls = [f'  <url><loc>{base}/</loc><priority>1.0</priority></url>']
    for cat in categories:
        urls.append(f'  <url><loc>{base}/{cat.slug}</loc><priority>0.8</priority></url>')
    for post in posts:
        if post.category:
            urls.append(
                f'  <url><loc>{base}/{post.category.slug}/{post.slug}</loc>'
                f'<lastmod>{post.updated_at.strftime("%Y-%m-%d")}</lastmod><priority>0.6</priority></url>'
            )
    urls.append(f'  <url><loc>{base}/gov-support/db</loc><priority>0.9</priority></url>')
    urls.append(f'  <url><loc>{base}/about</loc><priority>0.5</priority></url>')

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls)
    xml += "\n</urlset>"
    return Response(content=xml, media_type="application/xml")


@router.get("/robots.txt", response_class=Response)
async def robots():
    content = f"User-agent: *\nAllow: /\nSitemap: {settings.BASE_URL}/sitemap.xml\n"
    return Response(content=content, media_type="text/plain")
