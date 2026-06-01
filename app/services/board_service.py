from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.board import Board
from app.models.post import Post
from app.schemas.board import BoardCreate, BoardUpdate


def create_board(db: Session, board_data: BoardCreate) -> Board:
    """게시판 생성 (관리자만)"""
    board = Board(name=board_data.name)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def get_boards(db: Session) -> list[Board]:
    """게시판 목록 조회"""
    return db.query(Board).order_by(Board.created_at.asc()).all()


def get_board(db: Session, board_id: int) -> Board:
    """게시판 상세 조회"""
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise NotFoundException("존재하지 않는 게시판입니다.")
    return board


def update_board(db: Session, board_id: int, board_data: BoardUpdate) -> Board:
    """게시판 수정 (관리자만)"""
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise NotFoundException("존재하지 않는 게시판입니다.")
    if board_data.name is not None:
        board.name = board_data.name
    db.commit()
    db.refresh(board)
    return board


def delete_board(db: Session, board_id: int) -> None:
    """게시판 삭제 (관리자만)"""
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise NotFoundException("존재하지 않는 게시판입니다.")
    db.delete(board)
    db.commit()


def get_board_posts(db: Session, board_id: int) -> list[Post]:
    """특정 게시판의 게시글 목록 조회"""
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise NotFoundException("존재하지 않는 게시판입니다.")
    return (
        db.query(Post)
        .filter(Post.board_id == board_id)
        .order_by(Post.created_at.desc())
        .all()
    )
