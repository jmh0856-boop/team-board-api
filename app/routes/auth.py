from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
)
from app.database import get_db
from app.schemas.token import RefreshTokenRequest, Token
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """로그인 후 Access Token, Refresh Token 반환

    - OAuth2PasswordRequestForm 사용 → Swagger에서 바로 테스트 가능
    - form_data.username이 이메일 역할 (OAuth2 표준 필드명)
    - 인증 실패 시 401 반환
    """
    tokens = login_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(**tokens)


@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest):
    """Refresh Token으로 새 Access Token 재발급

    - Refresh Token 유효성 검증
    - type 필드가 refresh인지 확인
    - 새 Access Token, Refresh Token 반환
    """
    payload = decode_access_token(request.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 Refresh Token입니다.",
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 Refresh Token입니다.",
        )
    data = {"sub": user_id}
    return Token(
        access_token=create_access_token(data=data),
        refresh_token=create_refresh_token(data=data),
    )
