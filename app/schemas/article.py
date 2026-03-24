from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ArticleCreate(BaseModel):
    title: str = Field(..., max_length=300)
    summary: str = Field(...)
    content_md: str = Field(...)
    author: Optional[str] = Field(None, max_length=100)
    tag: Optional[str] = Field(None, max_length=50)
    category_slug: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=300)
    summary: Optional[str] = None
    content_md: Optional[str] = None
    author: Optional[str] = Field(None, max_length=100)
    tag: Optional[str] = Field(None, max_length=50)
    category_slug: Optional[str] = None


class ArticleAssign(BaseModel):
    category_slug: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    color: Optional[str] = None

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    status: str
    source: str
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    created_at: datetime
    message: str = ""


class ArticleDetail(BaseModel):
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    content_md: str
    content_html: str
    author: str
    tag: Optional[str] = None
    status: str
    source: str
    api_key_name: Optional[str] = None
    category_slug: Optional[str] = None
    category_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None


class ArticleListResponse(BaseModel):
    items: list[ArticleResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
