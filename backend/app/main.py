"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI  # type: ignore[import]
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import]

from app.core.config import settings  # type: ignore[import]
from app.core.database import engine, Base  # type: ignore[import]
# Ensure models are imported so SQLAlchemy can create tables
import app.models  # type: ignore[import]  # noqa: F401
from app.routes import auth, match, results  # type: ignore[import]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables …")
    Base.metadata.create_all(bind=engine)
    logger.info("Database ready.")
    yield


app = FastAPI(
    title="AI Resume Matcher API",
    description="Upload your resume, paste a job description, and get an AI-powered match analysis.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(match.router)
app.include_router(results.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
