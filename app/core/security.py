from datetime import datetime, timedelta

from jose import JWTError, jwt
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
    """JWT Access Token 생성

    - data: 토큰에 담을 정보 (보통 {"sub": str(user.id)})
    - 만료 시간은 settings에서 가져옴
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})  # 만료 시간을 payload에 추가
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
    except JWTError:
        # 위조되었거나 만료된 토큰 → None 반환 (호출부에서 401 처리)
        return None
