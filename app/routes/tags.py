import math

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import COMMON_RESPONSES, NOT_FOUND_RESPONSE
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import PostListBaseResponse, PostListResponse
from app.schemas.tag import TagBaseResponse, TagCreate, TagUpdate
from app.services.tag_service import get_posts_by_tag, set_post_tags

router = APIRouter(prefix="/posts/{post_id}/tags", tags=["태그"])


@router.post(
    "/",
    response_model=TagBaseResponse,
    summary="태그 등록",
    responses=COMMON_RESPONSES,
)
def create_tags(
    post_id: int,
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """태그 등록 - 작성자만 가능"""
    tags = set_post_tags(db, post_id, tag_data.names, current_user.id)
    return TagBaseResponse(
        data=tags,
        message="태그 등록 성공",
    )


@router.patch(
    "/",
    response_model=TagBaseResponse,
    summary="태그 수정",
    responses=COMMON_RESPONSES,
)
def update_tags(
    post_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """태그 수정 - 작성자만 가능 (전체 교체)"""
    tags = set_post_tags(db, post_id, tag_data.names, current_user.id)
    return TagBaseResponse(
        data=tags,
        message="태그 수정 성공",
    )


@router.get(
    "/filter",
    response_model=PostListBaseResponse,
    summary="태그 필터링",
    responses=NOT_FOUND_RESPONSE,
)
def filter_by_tag(
    tag_name: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    """특정 태그가 달린 게시글 목록 조회 - 누구나 가능"""
    posts, total = get_posts_by_tag(db, tag_name, page=page, size=size)
    return PostListBaseResponse(
        data=[PostListResponse.model_validate(post) for post in posts],
        total=total,
        page=page,
        size=size,
        total_pages=math.ceil(total / size) if size > 0 else 0,
        message="태그 필터링 성공",
    )
