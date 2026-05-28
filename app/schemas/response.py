from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """공통 응답 스키마"""

    success: bool = True
    data: Any = None
    message: str = "요청 성공"
