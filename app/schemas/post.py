from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    """게시글 생성 요청 스키마"""

    title: str
    content: str


class PostUpdate(BaseModel):
    """게시글 수정 요청 스키마 (일부만 수정 가능)"""

    title: str | None = None
    content: str | None = None


class PostAuthor(BaseModel):
    """게시글 작성자 정보"""

    id: int
    email: str

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """게시글 목록 응답 스키마"""

    id: int
    title: str
    author: PostAuthor
    created_at: datetime

    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    """게시글 상세 응답 스키마"""

    id: int
    title: str
    content: str
    author: PostAuthor
    created_at: datetime
    updated_at: datetime | None = None
    like_count: int = 0
    dislike_count: int = 0
    view_count: int = 0

    class Config:
        from_attributes = True
