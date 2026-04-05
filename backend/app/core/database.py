from sqlalchemy import create_engine  # type: ignore[import]
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # type: ignore[import]
from app.core.config import settings  # type: ignore[import]

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
