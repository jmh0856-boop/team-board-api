from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    """게시글 생성 요청 스키마"""

    title: str
    content: str
    board_id: int | None = None


class PostUpdate(BaseModel):
    """게시글 수정 요청 스키마 (일부만 수정 가능)"""

    title: str | None = None
    content: str | None = None
    board_id: int | None = None


class PostAuthor(BaseModel):
    """게시글 작성자 정보"""

    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class PostBoard(BaseModel):
    """게시글 게시판 정보"""

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PostListResponse(BaseModel):
    """게시글 목록 응답 스키마"""

    id: int
    title: str
    author: PostAuthor
    board: PostBoard | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDetailResponse(BaseModel):
    """게시글 상세 응답 스키마"""

    id: int
    title: str
    content: str
    author: PostAuthor
    board: PostBoard | None = None
    created_at: datetime
    updated_at: datetime | None = None
    like_count: int = 0
    dislike_count: int = 0
    view_count: int = 0

    model_config = ConfigDict(from_attributes=True)
