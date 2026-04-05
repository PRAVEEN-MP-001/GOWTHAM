"""Results route: retrieve past match results for the authenticated user."""
from fastapi import APIRouter, Depends  # type: ignore[import]
from sqlalchemy.orm import Session  # type: ignore[import]
from typing import List

from app.core.database import get_db  # type: ignore[import]
from app.core.security import get_current_user  # type: ignore[import]
from app.models.user import User  # type: ignore[import]
from app.models.result import Result  # type: ignore[import]
from app.schemas.result import ResultOut  # type: ignore[import]

router = APIRouter(tags=["results"])


@router.get("/results", response_model=List[ResultOut])
def get_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0,
):
    results = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .order_by(Result.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return results
