from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.schemas.response import BaseResponse
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_comments,
    get_replies,
    toggle_comment_like,
    update_comment,
)

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])


@router.post("/", response_model=BaseResponse)
def create(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 생성 - 로그인한 사용자만 가능"""
    comment = create_comment(db, post_id, comment_data, current_user.id)
    return BaseResponse(
        data=CommentResponse.model_validate(comment),
        message="댓글 생성 성공",
    )


@router.post("/{comment_id}/replies", response_model=BaseResponse)
def create_reply(
    post_id: int,
    comment_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """대댓글 생성 - 로그인한 사용자만 가능"""
    comment = create_comment(
        db, post_id, comment_data, current_user.id, parent_id=comment_id
    )
    return BaseResponse(
        data=CommentResponse.model_validate(comment),
        message="대댓글 생성 성공",
    )


@router.get("/", response_model=BaseResponse)
def get_list(post_id: int, db: Session = Depends(get_db)):
    """댓글 목록 조회 - 누구나 가능"""
    comments = get_comments(db, post_id)
    return BaseResponse(
        data=[CommentResponse.model_validate(comment) for comment in comments],
        message="댓글 목록 조회 성공",
    )


@router.get("/{comment_id}/replies", response_model=BaseResponse)
def get_reply_list(
    post_id: int, comment_id: int, db: Session = Depends(get_db)
):
    """대댓글 목록 조회 - 누구나 가능"""
    replies = get_replies(db, comment_id)
    return BaseResponse(
        data=[CommentResponse.model_validate(reply) for reply in replies],
        message="대댓글 목록 조회 성공",
    )


@router.patch("/{comment_id}", response_model=BaseResponse)
def update(
    post_id: int,
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 수정 - 작성자만 가능"""
    comment = update_comment(
        db, comment_id, comment_data.content, current_user.id
    )
    return BaseResponse(
        data=CommentResponse.model_validate(comment),
        message="댓글 수정 성공",
    )


@router.delete("/{comment_id}", response_model=BaseResponse)
def delete(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 삭제 - 작성자 또는 관리자만 가능"""
    delete_comment(
        db, comment_id, current_user.id, is_admin=current_user.is_admin
    )
    return BaseResponse(message="댓글 삭제 성공")


@router.post("/{comment_id}/like", response_model=BaseResponse)
def like(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 좋아요 - 로그인한 사용자만 가능"""
    result = toggle_comment_like(db, comment_id, current_user.id, is_like=True)
    return BaseResponse(message=result["message"])


@router.post("/{comment_id}/dislike", response_model=BaseResponse)
def dislike(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """댓글 싫어요 - 로그인한 사용자만 가능"""
    result = toggle_comment_like(
        db, comment_id, current_user.id, is_like=False
    )
    return BaseResponse(message=result["message"])
