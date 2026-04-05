"""Authentication routes: register and login."""
from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore[import]
from sqlalchemy.orm import Session  # type: ignore[import]
from passlib.context import CryptContext  # type: ignore[import]

from app.core.database import get_db  # type: ignore[import]
from app.core.security import create_access_token  # type: ignore[import]
from app.models.user import User  # type: ignore[import]
from app.schemas.auth import UserCreate, UserLogin, Token, UserOut  # type: ignore[import]

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    if len(payload.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters.",
        )
    user = User(email=payload.email, password_hash=_hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token)
