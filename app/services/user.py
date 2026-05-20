from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user_data: UserCreate):
    # 비밀번호 해시 처리는 나중에 보안 라이브러리(Passlib 등)로 추가 예정
    db_user = User(email=user_data.email, password=user_data.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
