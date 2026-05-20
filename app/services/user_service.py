import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_password_hash(password: str) -> str:
    # 비밀번호 bytes로 변환
    pwd_bytes = password.encode("utf-8")
    # salt 생성 및 해싱
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # DB 저장을 위해 다시 str로 변환
    return hashed.decode("utf-8")


def create_user(db: Session, user_data: UserCreate):
    # 비밀번호를 해싱해서 저장
    hashed_password = get_password_hash(user_data.password)

    # 모델에 저장할 때 password 대신 hashed_password 컬럼
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
