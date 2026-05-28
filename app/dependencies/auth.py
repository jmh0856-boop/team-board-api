from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidTokenException,
    PermissionDeniedException,
)
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

# 로그인 엔드포인트 경로 지정 (토큰을 어디서 발급받는지 Swagger에 표시됨)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """JWT 토큰을 검증하고 현재 로그인한 유저를 반환

    - 토큰이 없거나 유효하지 않으면 401 반환
    - 토큰은 유효하지만 유저가 DB에 없으면 401 반환
    """
    payload = decode_access_token(token)
    if payload is None:
        raise InvalidTokenException()

    # payload의 sub에서 user_id 추출
    user_id: str = payload.get("sub")
    if user_id is None:
        raise InvalidTokenException()

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise InvalidTokenException()

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """현재 로그인한 유저가 관리자인지 확인

    - 관리자가 아니면 403 반환
    """
    if not current_user.is_admin:
        raise PermissionDeniedException()
    return current_user
