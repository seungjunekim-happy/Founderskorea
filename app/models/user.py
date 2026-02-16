from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, unique=True, index=True)
    industry = Column(String(200), nullable=True)
    business_stage = Column(String(100), nullable=True)
    business_size = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    interests = Column(Text, nullable=True)  # comma-separated
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
