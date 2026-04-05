from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text  # type: ignore[import]
from sqlalchemy.orm import relationship  # type: ignore[import]
from sqlalchemy.sql import func  # type: ignore[import]
from sqlalchemy.dialects.postgresql import JSONB  # type: ignore[import]
from app.core.database import Base  # type: ignore[import]


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    match_score = Column(Float, nullable=False)
    matched_skills = Column(JSONB, default=list)
    missing_skills = Column(JSONB, default=list)
    suggestions = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="results")
