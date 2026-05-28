from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostDetailResponse,
    PostListResponse,
    PostUpdate,
)
from app.schemas.response import BaseResponse
from app.services.post_service import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    toggle_like,
    update_post,
)

router = APIRouter(prefix="/posts", tags=["게시글"])


@router.post("/", response_model=BaseResponse, summary="게시글 생성")
def create(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 생성 - 로그인한 사용자만 가능"""
    post = create_post(db, post_data, current_user.id)
    return BaseResponse(
        data=PostDetailResponse.model_validate(post),
        message="게시글 생성 성공",
    )


@router.get("/", response_model=BaseResponse, summary="게시글 목록 조회")
def get_list(db: Session = Depends(get_db)):
    """게시글 목록 조회 - 누구나 가능"""
    posts = get_posts(db)
    return BaseResponse(
        data=[PostListResponse.model_validate(post) for post in posts],
        message="게시글 목록 조회 성공",
    )


@router.get("/{post_id}", response_model=BaseResponse, summary="게시글 상세 조회")
def get_detail(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회 - 누구나 가능 (조회수 증가)"""
    post = get_post(db, post_id)
    like_count = sum(1 for like in post.likes if like.is_like)
    dislike_count = sum(1 for like in post.likes if not like.is_like)
    return BaseResponse(
        data=PostDetailResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            author=post.author,
            board=post.board,
            created_at=post.created_at,
            updated_at=post.updated_at,
            view_count=post.view_count,
            like_count=like_count,
            dislike_count=dislike_count,
        ),
        message="게시글 상세 조회 성공",
    )


@router.patch("/{post_id}", response_model=BaseResponse, summary="게시글 수정")
def update(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 수정 - 작성자만 가능"""
    post = update_post(db, post_id, post_data, current_user.id)
    return BaseResponse(
        data=PostDetailResponse.model_validate(post),
        message="게시글 수정 성공",
    )


@router.delete("/{post_id}", response_model=BaseResponse, summary="게시글 삭제")
def delete(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """게시글 삭제 - 작성자 or 관리자만 가능"""
    delete_post(db, post_id, current_user.id, is_admin=current_user.is_admin)
    return BaseResponse(message="게시글 삭제 성공")


@router.post("/{post_id}/like", response_model=BaseResponse, summary="게시글 좋아요")
def like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """좋아요 - 로그인한 사용자만 가능"""
    result = toggle_like(db, post_id, current_user.id, is_like=True)
    return BaseResponse(message=result["message"])


@router.post(
    "/{post_id}/dislike", response_model=BaseResponse, summary="게시글 싫어요"
)
def dislike(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """싫어요 - 로그인한 사용자만 가능"""
    result = toggle_like(db, post_id, current_user.id, is_like=False)
    return BaseResponse(message=result["message"])
