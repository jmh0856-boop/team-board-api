from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException
from app.database import get_db
from app.models.user import User
from app.schemas.response import BaseResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["사용자"])


@router.post("/", response_model=BaseResponse, summary="회원가입")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise DuplicateEmailException()

    db_user = create_user(db, user)
    return BaseResponse(
        data=UserResponse.model_validate(db_user),
        message="회원가입 성공",
    )
