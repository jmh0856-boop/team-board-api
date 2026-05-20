from pydantic import BaseModel


class Token(BaseModel):
    """로그인 성공 시 반환하는 토큰 응답 스키마"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT payload에서 추출한 데이터 스키마

    - user_id: 토큰에서 꺼낸 사용자 식별자
    """

    user_id: int | None = None
