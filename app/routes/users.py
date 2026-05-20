from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateEmailException
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise DuplicateEmailException()

    db_user = create_user(db, user)
    return db_user
