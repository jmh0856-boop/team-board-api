from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    content: str  # 삭제된 경우 메세지로 대체
    author: CommentAuthor
    post_id: int
    parent_id: int | None = None  # 대댓글인 경우 부모 댓글 id
    is_deleted: bool
    like_count: int = 0
    dislike_count: int = 0
    replies: list[CommentResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    """댓글 수정 요청 스키마"""  # 추가

    content: str
