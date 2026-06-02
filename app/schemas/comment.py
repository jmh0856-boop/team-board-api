from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class CommentCreate(BaseModel):
    """댓글 생성 요청 스키마"""

    content: str


class CommentAuthor(BaseModel):
    """댓글 작성자 정보"""

    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    """댓글 응답 스키마"""

    id: int
    content: str
    author: CommentAuthor
    post_id: int
    parent_id: int | None = None
    is_deleted: bool
    deleted_by: str | None = None
    like_count: int = 0
    dislike_count: int = 0
    replies: list[CommentResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def apply_deleted_message(self) -> CommentResponse:
        """삭제된 댓글 메시지 처리"""
        if self.is_deleted:
            if self.deleted_by == "admin":
                self.content = "관리자에 의해 삭제된 댓글입니다."
            else:
                self.content = "사용자에 의해 삭제된 댓글입니다."
        return self


class CommentUpdate(BaseModel):
    """댓글 수정 요청 스키마"""

    content: str


class CommentBaseResponse(BaseModel):
    """댓글 단건 응답 스키마"""

    success: bool = True
    data: CommentResponse | None = None
    message: str = "요청 성공"


class CommentListBaseResponse(BaseModel):
    """댓글 목록 응답 스키마"""

    success: bool = True
    data: list[CommentResponse] = []
    message: str = "요청 성공"
