from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 서비스 계층의 create_user 함수 호출
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return db_user
