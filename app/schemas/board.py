from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BoardCreate(BaseModel):
    """게시판 생성 요청 스키마"""

    name: str


class BoardUpdate(BaseModel):
    """게시판 수정 요청 스키마"""

    name: str | None = None


class BoardResponse(BaseModel):
    """게시판 응답 스키마"""

    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
