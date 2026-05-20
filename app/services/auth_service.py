from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """이메일과 비밀번호로 사용자 인증

    - 이메일로 유저 조회 → 없으면 None
    - 비밀번호 검증 → 틀리면 None
    - 모두 통과하면 User 객체 반환
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_user(db: Session, email: str, password: str) -> str | None:
    """로그인 처리 후 JWT Access Token 반환

    - 인증 실패 시 None 반환 → 라우터에서 401 처리
    - sub에 user_id를 문자열로 저장 (JWT 표준)
    """
    user = authenticate_user(db, email, password)
    if not user:
        return None
    data = {"sub": str(user.id)}
    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
