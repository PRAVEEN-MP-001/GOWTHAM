from pydantic import BaseModel  # type: ignore[import]
from typing import List
from datetime import datetime


class MatchRequest(BaseModel):
    job_description: str


class MatchResult(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]


class ResultOut(BaseModel):
    id: int
    resume_text: str
    job_description: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    created_at: datetime

    model_config = {"from_attributes": True}
