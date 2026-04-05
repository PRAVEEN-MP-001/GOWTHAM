from sqlalchemy import Column, Integer, String, DateTime  # type: ignore[import]
from sqlalchemy.orm import relationship  # type: ignore[import]
from sqlalchemy.sql import func  # type: ignore[import]
from app.core.database import Base  # type: ignore[import]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    results = relationship("Result", back_populates="user", cascade="all,delete")
