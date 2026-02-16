from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class GovSupportProgram(Base):
    __tablename__ = "gov_support_programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), nullable=False, unique=True, index=True)
    organization = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    support_type = Column(String(100), nullable=False)  # 자금, 멘토링, 교육, 공간, 컨설팅
    region = Column(String(100), nullable=False)  # 서울, 경기, 부산, 전국 등
    industry = Column(String(200), nullable=True)  # 업종
    business_stage = Column(String(100), nullable=True)  # 예비창업, 초기, 성장기 등
    business_size = Column(String(100), nullable=True)  # 1인, 소기업, 중기업
    funding_amount = Column(String(200), nullable=True)  # 지원금액 텍스트
    deadline = Column(Date, nullable=True)
    start_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="모집중")  # 모집중, 마감, 상시
    url = Column(String(500), nullable=True)
    keywords = Column(Text, nullable=True)  # comma-separated
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    reviews = relationship("ProgramReview", back_populates="program", lazy="selectin")
    application_kit = relationship("ApplicationKit", back_populates="program", uselist=False, lazy="selectin")


class ProgramReview(Base):
    __tablename__ = "program_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("gov_support_programs.id"), nullable=False)
    nickname = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    content = Column(Text, nullable=False)
    success_tag = Column(String(100), nullable=True)  # 선정됨, 탈락, 진행중
    tip = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    program = relationship("GovSupportProgram", back_populates="reviews")


class ApplicationKit(Base):
    __tablename__ = "application_kits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("gov_support_programs.id"), nullable=False, unique=True)
    checklist_md = Column(Text, nullable=False, default="")
    checklist_html = Column(Text, nullable=False, default="")
    guide_md = Column(Text, nullable=False, default="")
    guide_html = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    program = relationship("GovSupportProgram", back_populates="application_kit")
