from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_comments,
    get_replies,
    toggle_comment_like,
    update_comment,
)

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.post("/", response_model=CommentResponse)
def create(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """댓글 생성 - 로그인한 사용자만 가능"""
    return create_comment(db, post_id, comment_data, current_user.id)


@router.post("/{comment_id}/replies", response_model=CommentResponse)
def create_reply(
    post_id: int,
    comment_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """대댓글 생성 - 로그인한 사용자만 가능"""
    return create_comment(
        db, post_id, comment_data, current_user.id, parent_id=comment_id
    )


@router.get("/", response_model=list[CommentResponse])
def get_list(post_id: int, db: Session = Depends(get_db)):
    """댓글 목록 조회 - 누구나 가능"""
    return get_comments(db, post_id)


@router.get("/{comment_id}/replies", response_model=list[CommentResponse])
def get_reply_list(
    post_id: int, comment_id: int, db: Session = Depends(get_db)
):
    """대댓글 목록 조회 - 누구나 가능"""
    return get_replies(db, comment_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update(
    post_id: int,
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 수정 - 작성자만 가능"""
    return update_comment(
        db, comment_id, comment_data.content, current_user.id
    )


@router.delete("/{comment_id}")
def delete(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """댓글 삭제 - 작성자 또는 관리자만 가능"""
    delete_comment(
        db, comment_id, current_user.id, is_admin=current_user.is_admin
    )
    return {"success": True, "message": "댓글이 삭제되었습니다."}


@router.post("/{comment_id}/like")
def like(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """댓글 좋아요 - 로그인한 사용자만 가능"""
    return toggle_comment_like(db, comment_id, current_user.id, is_like=True)


@router.post("/{comment_id}/dislike")
def dislike(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인 필요
):
    """댓글 싫어요 - 로그인한 사용자만 가능"""
    return toggle_comment_like(db, comment_id, current_user.id, is_like=False)
