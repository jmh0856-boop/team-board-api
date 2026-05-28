from pydantic import BaseModel


class Token(BaseModel):
    """로그인 성공 시 반환하는 토큰 응답 스키마"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Access Token 재발급 요청 스키마"""

    refresh_token: str
