from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_by = Column(String, nullable=True)  # "user" 또는 "admin"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", back_populates="parent")
    parent = relationship(
        "Comment", back_populates="replies", remote_side=[id]
    )
    comment_likes = relationship(
        "CommentLike", back_populates="comment", cascade="all, delete-orphan"
    )
