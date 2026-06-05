from datetime import datetime

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from app.schemas.tag import TagResponse


class PostCreate(BaseModel):
    """게시글 생성 요청 스키마"""

    title: str
    content: str
    board_id: int | None = None
    tag_names: list[str] = []


class PostUpdate(BaseModel):
    """게시글 수정 요청 스키마 (일부만 수정 가능)"""

    title: str | None = None
    content: str | None = None
    board_id: int | None = None


class PostAuthor(BaseModel):
    """게시글 작성자 정보"""

    user_id: int = Field(validation_alias=AliasPath("id"))  # 수정
    email: str

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True
    )  # 수정


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
    tags: list[TagResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def extract_tags(cls, data: object) -> object:
        """PostTag에서 Tag 정보 추출"""
        if not hasattr(data, "__dict__"):
            return data
        result = {}
        result["id"] = data.id
        result["title"] = data.title
        result["author"] = data.author
        result["board"] = data.board
        result["created_at"] = data.created_at
        result["tags"] = [pt.tag for pt in data.tags]
        return result


class PostDetailResponse(BaseModel):
    """게시글 상세 응답 스키마"""

    id: int
    title: str
    content: str
    author: PostAuthor
    board: PostBoard | None = None
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: datetime | None = None
    like_count: int = 0
    dislike_count: int = 0
    view_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def calculate_likes(cls, data: object) -> object:
        """좋아요/싫어요 수 계산 및 태그 추출"""
        if not hasattr(data, "__dict__"):
            return data
        result = {}
        result["id"] = data.id
        result["title"] = data.title
        result["content"] = data.content
        result["author"] = data.author
        result["board"] = data.board
        result["created_at"] = data.created_at
        result["updated_at"] = data.updated_at
        result["view_count"] = data.view_count
        result["like_count"] = sum(1 for like in data.likes if like.is_like)
        result["dislike_count"] = sum(
            1 for like in data.likes if not like.is_like
        )
        result["tags"] = [pt.tag for pt in data.tags]
        return result


class PostBaseResponse(BaseModel):
    """게시글 단건 응답 스키마"""

    success: bool = True
    data: PostDetailResponse | None = None
    message: str = "요청 성공"


class PostListBaseResponse(BaseModel):
    """게시글 목록 응답 스키마"""

    success: bool = True
    data: list[PostListResponse] = []
    message: str = "요청 성공"
