from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """에러 응답 스키마"""

    success: bool = False
    message: str


# 인증 필요한 라우터 공통 에러 응답
COMMON_RESPONSES = {
    401: {"model": ErrorResponse, "description": "인증 실패"},
    403: {"model": ErrorResponse, "description": "권한 없음"},
    404: {"model": ErrorResponse, "description": "리소스 없음"},
}

# 인증 불필요한 라우터 에러 응답
NOT_FOUND_RESPONSE = {
    404: {"model": ErrorResponse, "description": "리소스 없음"},
}

# 인증만 필요한 라우터 에러 응답
AUTH_RESPONSES = {
    401: {"model": ErrorResponse, "description": "인증 실패"},
}

# 이메일 중복 에러 응답
DUPLICATE_EMAIL_RESPONSE = {
    400: {"model": ErrorResponse, "description": "이메일 중복"},
}
