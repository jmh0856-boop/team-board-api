from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.token import Token
from app.services.auth_service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """로그인 후 JWT Access Token 반환

    - OAuth2PasswordRequestForm 사용 → Swagger에서 바로 테스트 가능
    - form_data.username이 이메일 역할 (OAuth2 표준 필드명)
    - 인증 실패 시 401 반환
    """
    access_token = login_user(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=access_token)
