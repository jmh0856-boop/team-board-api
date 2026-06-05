from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # 관계 설정
    posts = relationship("PostTag", back_populates="tag")


class PostTag(Base):
    __tablename__ = "post_tags"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

    # 같은 게시글에 같은 태그 중복 불가
    __table_args__ = (
        UniqueConstraint("post_id", "tag_id", name="unique_post_tag"),
    )

    # 관계 설정
    post = relationship("Post", back_populates="tags")
    tag = relationship("Tag", back_populates="posts")
