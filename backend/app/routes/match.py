"""Match route: accepts resume file + job description, returns analysis."""
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException, status  # type: ignore[import]
from sqlalchemy.orm import Session  # type: ignore[import]

from app.core.database import get_db  # type: ignore[import]
from app.core.security import get_current_user  # type: ignore[import]
from app.models.user import User  # type: ignore[import]
from app.models.result import Result  # type: ignore[import]
from app.schemas.result import MatchResult  # type: ignore[import]
from app.services.file_parser import extract_text_from_file  # type: ignore[import]
from app.services.skill_extractor import extract_skills, extract_missing_skills  # type: ignore[import]
from app.services.matcher import compute_match_score  # type: ignore[import]
from app.services.suggestions import generate_suggestions  # type: ignore[import]

router = APIRouter(tags=["match"])


@router.post("/match", response_model=MatchResult)
async def match_resume(
    job_description: str = Form(..., min_length=50),
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    # 1. Parse resume
    resume_text = await extract_text_from_file(resume_file)

    # 2. Compute hybrid match score
    final_score, _kw, _sem = compute_match_score(resume_text, job_description)
    match_pct = round(final_score * 100, 2)

    # 3. Skill analysis — vocab match for matched, full gap analysis for missing
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    matched = sorted(resume_skills & job_skills)
    missing = extract_missing_skills(resume_text, job_description)

    # 4. Suggestions
    suggestions = generate_suggestions(missing)

    # 5. Persist
    result = Result(
        user_id=current_user.id,
        resume_text=resume_text,
        job_description=job_description,
        match_score=match_pct,
        matched_skills=matched,
        missing_skills=missing,
        suggestions=suggestions,
    )
    try:
        db.add(result)
        db.commit()
        db.refresh(result)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save results. Please try again.",
        ) from exc

    return MatchResult(
        match_score=match_pct,
        matched_skills=matched,
        missing_skills=missing,
        suggestions=suggestions,
    )
