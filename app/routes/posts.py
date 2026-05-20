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
from app.services.post_service import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    toggle_like,
    update_post,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostDetailResponse)
def create(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """게시글 생성 - 로그인한 사용자만 가능"""
    return create_post(db, post_data, current_user.id)


@router.get("/", response_model=list[PostListResponse])
def get_list(db: Session = Depends(get_db)):
    """게시글 목록 조회 - 누구나 가능"""
    return get_posts(db)


@router.get("/{post_id}", response_model=PostDetailResponse)
def get_detail(post_id: int, db: Session = Depends(get_db)):
    """게시글 상세 조회 - 누구나 가능 (조회수 증가)"""
    post = get_post(db, post_id)
    like_count = sum(1 for like in post.likes if like.is_like)
    dislike_count = sum(1 for like in post.likes if not like.is_like)
    return PostDetailResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        created_at=post.created_at,
        updated_at=post.updated_at,
        view_count=post.view_count,
        like_count=like_count,
        dislike_count=dislike_count,
    )


@router.patch("/{post_id}", response_model=PostDetailResponse)
def update(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """게시글 수정 - 작성자만 가능"""
    return update_post(db, post_id, post_data, current_user.id)


@router.delete("/{post_id}")
def delete(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """게시글 삭제 - 작성자만 가능"""
    delete_post(db, post_id, current_user.id)
    return {"success": True, "message": "게시글이 삭제되었습니다."}


@router.post("/{post_id}/like")
def like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """좋아요 - 로그인한 사용자만 가능"""
    return toggle_like(db, post_id, current_user.id, is_like=True)


@router.post("/{post_id}/dislike")
def dislike(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """싫어요 - 로그인한 사용자만 가능"""
    return toggle_like(db, post_id, current_user.id, is_like=False)
