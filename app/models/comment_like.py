from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    is_like = Column(Boolean, nullable=False)  # True: 좋아요, False: 싫어요
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 한 유저가 한 댓글에 한 번만 좋아요/싫어요 가능
    __table_args__ = (
        UniqueConstraint(
            "user_id", "comment_id", name="unique_user_comment_like"
        ),
    )

    # 관계 설정
    user = relationship("User", back_populates="comment_likes")
    comment = relationship("Comment", back_populates="comment_likes")
