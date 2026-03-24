import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class ArticleStatus(str, enum.Enum):
    draft = "draft"
    review = "review"
    published = "published"
    archived = "archived"


class ArticleSource(str, enum.Enum):
    seed = "seed"
    api = "api"
    editor = "editor"
    manual = "manual"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), nullable=False, unique=True, index=True)
    summary = Column(Text, nullable=True)
    content_md = Column(Text, nullable=False, default="")
    content_html = Column(Text, nullable=False, default="")
    author = Column(String(100), nullable=False, default="Founderskorea Team")
    tag = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="draft", index=True)
    source = Column(String(20), nullable=False, default="manual")
    api_key_name = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    @property
    def is_published(self) -> bool:
        return self.status == ArticleStatus.published.value

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="posts", lazy="selectin")
