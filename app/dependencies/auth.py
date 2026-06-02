from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import (
    InvalidTokenException,
    PermissionDeniedException,
    UnauthorizedException,
)
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """JWT 토큰을 검증하고 현재 로그인한 유저를 반환"""
    if credentials is None:
        raise UnauthorizedException(detail="인증이 필요합니다.")

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise InvalidTokenException()

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
    """현재 로그인한 유저가 관리자인지 확인"""
    if not current_user.is_admin:
        raise PermissionDeniedException()
    return current_user
