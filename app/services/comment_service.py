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
    parent_id: int | None = None,  # 대댓글인 경우 부모 댓글 id
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


def _apply_like_count(comment: Comment) -> None:
    """좋아요/싫어요 수 계산"""  # 추가
    comment.like_count = sum(
        1 for like in comment.comment_likes if like.is_like
    )
    comment.dislike_count = sum(
        1 for like in comment.comment_likes if not like.is_like
    )


def get_comments(db: Session, post_id: int) -> list[Comment]:
    """게시글의 댓글 목록 조회 (대댓글 포함)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")

    comments = (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.parent_id.is_(None))
        .order_by(Comment.created_at.asc())
        .all()
    )

    for comment in comments:
        _apply_deleted_message(comment)
        _apply_like_count(comment)
        for reply in comment.replies:
            _apply_deleted_message(reply)
            _apply_like_count(reply)

    return comments


def _apply_deleted_message(comment: Comment) -> None:
    """삭제된 댓글 메시지 처리"""
    if comment.is_deleted:
        if comment.deleted_by == "admin":
            comment.content = "관리자에 의해 삭제된 댓글입니다."
        else:
            comment.content = "사용자에 의해 삭제된 댓글입니다."


def get_replies(db: Session, comment_id: int) -> list[Comment]:
    """대댓글 목록 조회"""  # 추가
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")

    replies = (
        db.query(Comment)
        .filter(Comment.parent_id == comment_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    for reply in replies:
        _apply_deleted_message(reply)
    return replies


def update_comment(
    db: Session, comment_id: int, content: str, user_id: int
) -> Comment:
    """댓글 수정 - 작성자만 가능"""  # 추가
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise NotFoundException("존재하지 않는 댓글입니다.")
    if comment.user_id != user_id:
        raise PermissionDeniedException()
    if comment.is_deleted:  # 삭제된 댓글은 수정 불가
        raise NotFoundException("삭제된 댓글은 수정할 수 없습니다.")

    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(
    db: Session, comment_id: int, user_id: int, is_admin: bool = False
) -> None:
    """댓글 삭제 - 소프트 삭제

    - 작성자 삭제 → deleted_by = "user"
    - 관리자 삭제 → deleted_by = "admin"
    """
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
    """댓글 좋아요/싫어요 토글

    - 같은 버튼 누르면 취소
    - 좋아요 상태에서 싫어요 또는 반대면 409 에러
    """  # 추가
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
