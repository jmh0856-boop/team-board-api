from sqlalchemy.orm import Session

from app.core.security import get_password_hash  # passlib 사용
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate):
    # security.py의 get_password_hash 사용 (passlib 기반)
    hashed_password = get_password_hash(user_data.password)

    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
