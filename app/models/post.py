from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


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
    is_published = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="posts", lazy="selectin")
