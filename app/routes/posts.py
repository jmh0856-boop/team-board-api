from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import (
    PostBaseResponse,
    PostCreate,
    PostDetailResponse,
    PostListBaseResponse,
    PostListResponse,
    PostUpdate,
)
from app.services.post_service import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    toggle_like,
    update_post,
)

router = APIRouter(prefix="/posts", tags=["게시글"])


@router.post("/", response_model=PostBaseResponse, summary="게시글 생성")
def create(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 생성 - 로그인한 사용자만 가능"""
    post = create_post(db, post_data, current_user.id)
    return PostBaseResponse(
        data=PostDetailResponse.model_validate(post),
        message="게시글 생성 성공",
    )


@router.get("/", response_model=PostListBaseResponse, summary="게시글 목록 조회")
def get_list(db: Session = Depends(get_db)):
    """게시글 목록 조회 - 누구나 가능"""
    posts = get_posts(db)
    return PostListBaseResponse(
        data=[PostListResponse.model_validate(post) for post in posts],
        message="게시글 목록 조회 성공",
    )


@router.get("/{post_id}", response_model=PostBaseResponse, summary="게시글 상세 조회")
def get_detail(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회 - 누구나 가능 (조회수 증가)"""
    post = get_post(db, post_id)
    return PostBaseResponse(
        data=PostDetailResponse.model_validate(post),
        message="게시글 상세 조회 성공",
    )


@router.patch("/{post_id}", response_model=PostBaseResponse, summary="게시글 수정")
def update(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 수정 - 작성자만 가능"""
    post = update_post(db, post_id, post_data, current_user.id)
    return PostBaseResponse(
        data=PostDetailResponse.model_validate(post),
        message="게시글 수정 성공",
    )


@router.delete("/{post_id}", response_model=PostBaseResponse, summary="게시글 삭제")
def delete(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 삭제 - 작성자 or 관리자만 가능"""
    delete_post(db, post_id, current_user.id, is_admin=current_user.is_admin)
    return PostBaseResponse(message="게시글 삭제 성공")


@router.post(
    "/{post_id}/like", response_model=PostBaseResponse, summary="게시글 좋아요"
)
def like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """좋아요 - 로그인한 사용자만 가능"""
    result = toggle_like(db, post_id, current_user.id, is_like=True)
    return PostBaseResponse(message=result["message"])


@router.post(
    "/{post_id}/dislike", response_model=PostBaseResponse, summary="게시글 싫어요"
)
def dislike(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """싫어요 - 로그인한 사용자만 가능"""
    result = toggle_like(db, post_id, current_user.id, is_like=False)
    return PostBaseResponse(message=result["message"])
