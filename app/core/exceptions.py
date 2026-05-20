from fastapi import HTTPException, status


class PermissionDeniedException(HTTPException):
    """권한 없음 - 작성자가 아닌 경우"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다.",
        )


class NotFoundException(HTTPException):
    """리소스 없음"""

    def __init__(self, detail: str = "존재하지 않는 리소스입니다."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ConflictException(HTTPException):
    """충돌 - 좋아요/싫어요 상태 충돌"""

    def __init__(self, detail: str = "이미 다른 반응이 존재합니다."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class DuplicateEmailException(HTTPException):
    """이메일 중복"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다.",
        )
