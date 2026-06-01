from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.core.config import settings

# 비밀번호 해싱 알고리즘 설정 (bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 DB에 저장된 해시 비밀번호를 비교"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호를 bcrypt로 해싱하여 반환"""
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """JWT Access Token 생성 (단기 토큰)"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    """JWT Refresh Token 생성 (장기 토큰)

    - Access Token 만료 시 재발급에 사용
    - 만료 시간은 7일로 고정
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict | None:
    """JWT 토큰을 디코딩하여 payload 반환

    - 토큰이 유효하지 않거나 만료된 경우 None 반환
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except InvalidTokenError:
        # 위조되었거나 만료된 토큰 → None 반환 (호출부에서 401 처리)
        return None
