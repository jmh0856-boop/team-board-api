from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
)
from app.models.comment import Comment
from app.models.comment_like import CommentLike
from app.models.post import Post
from app.schemas.comment import CommentCreate


def create_comment(
    db: Session,
    post_id: int,
    comment_data: CommentCreate,
    user_id: int,
    parent_id: int | None = None,
) -> Comment:
    """댓글 및 대댓글 생성"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")

    if parent_id:
        parent = db.query(Comment).filter(Comment.id == parent_id).first()
        if not parent:
            raise NotFoundException("존재하지 않는 댓글입니다.")

    comment = Comment(
        content=comment_data.content,
        user_id=user_id,
        post_id=post_id,
        parent_id=parent_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, post_id: int) -> list[Comment]:
    """게시글의 댓글 목록 조회 (대댓글 포함)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")

    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.parent_id.is_(None))
        .order_by(Comment.created_at.asc())
        .all()
    )


def get_replies(db: Session, comment_id: int) -> list[Comment]:
    """대댓글 목록 조회"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")

    return (
        db.query(Comment)
        .filter(Comment.parent_id == comment_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


def update_comment(
    db: Session, comment_id: int, content: str, user_id: int
) -> Comment:
    """댓글 수정 - 작성자만 가능"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")
    if comment.user_id != user_id:
        raise PermissionDeniedException()
    if comment.is_deleted:
        raise NotFoundException("삭제된 댓글은 수정할 수 없습니다.")

    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(
    db: Session, comment_id: int, user_id: int, is_admin: bool = False
) -> None:
    """댓글 삭제 - 소프트 삭제"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")
    if not is_admin and comment.user_id != user_id:
        raise PermissionDeniedException()

    comment.is_deleted = True
    comment.deleted_by = "admin" if is_admin else "user"
    db.commit()
    db.refresh(comment)


def toggle_comment_like(
    db: Session, comment_id: int, user_id: int, is_like: bool
) -> dict:
    """댓글 좋아요/싫어요 토글"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")

    existing = (
        db.query(CommentLike)
        .filter(
            CommentLike.user_id == user_id,
            CommentLike.comment_id == comment_id,
        )
        .first()
    )

    if existing:
        if existing.is_like == is_like:
            db.delete(existing)
            db.commit()
            action = "좋아요" if is_like else "싫어요"
            return {"message": f"{action}가 취소되었습니다."}
        else:
            action = "좋아요" if existing.is_like else "싫어요"
            raise ConflictException(f"{action} 상태에서 다른 반응을 누를 수 없습니다.")

    like = CommentLike(user_id=user_id, comment_id=comment_id, is_like=is_like)
    db.add(like)
    db.commit()
    action = "좋아요" if is_like else "싫어요"
    return {"message": f"{action}를 눌렀습니다."}
