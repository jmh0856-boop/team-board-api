from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    PermissionDeniedException,
)
from app.models.like import Like
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


def create_post(db: Session, post_data: PostCreate, user_id: int) -> Post:
    """게시글 생성"""
    post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=user_id,
        board_id=post_data.board_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session) -> list[Post]:
    """게시글 목록 조회"""
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post(db: Session, post_id: int) -> Post:
    """게시글 상세 조회 (조회수 증가)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post


def update_post(
    db: Session, post_id: int, post_data: PostUpdate, user_id: int
) -> Post:
    """게시글 수정 (작성자만 가능)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")
    if post.user_id != user_id:
        raise PermissionDeniedException()
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post


def delete_post(
    db: Session, post_id: int, user_id: int, is_admin: bool = False
) -> None:
    """게시글 삭제 (작성자 or 관리자만 가능)"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")
    if not is_admin and post.user_id != user_id:
        raise PermissionDeniedException()
    db.delete(post)
    db.commit()


def toggle_like(
    db: Session, post_id: int, user_id: int, is_like: bool
) -> dict:
    """좋아요/싫어요 토글

    - 같은 버튼 누르면 취소 (행 삭제)
    - 좋아요 상태에서 싫어요 또는 반대면 409 에러
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")

    existing = (
        db.query(Like)
        .filter(Like.user_id == user_id, Like.post_id == post_id)
        .first()
    )

    if existing:
        if existing.is_like == is_like:
            # 같은 버튼 → 취소
            db.delete(existing)
            db.commit()
            action = "좋아요" if is_like else "싫어요"
            return {"message": f"{action}가 취소되었습니다."}
        else:
            # 다른 버튼 → 충돌
            action = "좋아요" if existing.is_like else "싫어요"
            raise ConflictException(f"{action} 상태에서 다른 반응을 누를 수 없습니다.")

    # 새로 저장
    like = Like(user_id=user_id, post_id=post_id, is_like=is_like)
    db.add(like)
    db.commit()
    action = "좋아요" if is_like else "싫어요"
    return {"message": f"{action}를 눌렀습니다."}
