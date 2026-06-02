from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException
from app.core.responses import DUPLICATE_EMAIL_RESPONSE
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserBaseResponse, UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["사용자"])


@router.post(
    "/",
    response_model=UserBaseResponse,
    summary="회원가입",
    responses=DUPLICATE_EMAIL_RESPONSE,
)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise DuplicateEmailException()

    db_user = create_user(db, user)
    return UserBaseResponse(
        data=UserResponse.model_validate(db_user),
        message="회원가입 성공",
    )
