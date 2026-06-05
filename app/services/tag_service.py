from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, PermissionDeniedException
from app.models.post import Post
from app.models.tag import PostTag, Tag


def get_or_create_tag(db: Session, name: str) -> Tag:
    """태그가 있으면 반환, 없으면 생성"""
    tag = db.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        db.flush()  # id 생성을 위해 flush
    return tag


def set_post_tags(
    db: Session, post_id: int, tag_names: list[str], user_id: int
) -> list[Tag]:
    """게시글 태그 등록/수정 (전체 교체)

    - 기존 태그 전부 삭제 후 새 태그 등록
    - 작성자만 가능
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise NotFoundException("존재하지 않는 게시글입니다.")
    if post.user_id != user_id:
        raise PermissionDeniedException()

    # 기존 태그 전부 삭제
    db.query(PostTag).filter(PostTag.post_id == post_id).delete()

    # 새 태그 등록
    tags = []
    for name in tag_names:
        tag = get_or_create_tag(db, name.strip())
        post_tag = PostTag(post_id=post_id, tag_id=tag.id)
        db.add(post_tag)
        tags.append(tag)

    db.commit()
    return tags


def get_posts_by_tag(db: Session, tag_name: str) -> list[Post]:
    """특정 태그가 달린 게시글 목록 조회"""
    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        raise NotFoundException("존재하지 않는 태그입니다.")

    return (
        db.query(Post)
        .join(PostTag)
        .filter(PostTag.tag_id == tag.id)
        .order_by(Post.created_at.desc())
        .all()
    )
