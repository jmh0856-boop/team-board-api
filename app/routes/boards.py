from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.board import BoardCreate, BoardResponse, BoardUpdate
from app.schemas.post import PostListResponse
from app.services.board_service import (
    create_board,
    delete_board,
    get_board,
    get_board_posts,
    get_boards,
    update_board,
)

router = APIRouter(prefix="/boards", tags=["boards"])


@router.post("/", response_model=BoardResponse)
def create(
    board_data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # 관리자만
):
    """게시판 생성 - 관리자만 가능"""
    return create_board(db, board_data)


@router.get("/", response_model=list[BoardResponse])
def get_list(db: Session = Depends(get_db)):
    """게시판 목록 조회 - 누구나 가능"""
    return get_boards(db)


@router.get("/{board_id}", response_model=BoardResponse)
def get_detail(board_id: int, db: Session = Depends(get_db)):
    """게시판 상세 조회 - 누구나 가능"""
    return get_board(db, board_id)


@router.patch("/{board_id}", response_model=BoardResponse)
def update(
    board_id: int,
    board_data: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # 관리자만
):
    """게시판 수정 - 관리자만 가능"""
    return update_board(db, board_id, board_data)


@router.delete("/{board_id}")
def delete(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),  # 관리자만
):
    """게시판 삭제 - 관리자만 가능"""
    delete_board(db, board_id)
    return {"success": True, "message": "게시판이 삭제되었습니다."}


@router.get("/{board_id}/posts", response_model=list[PostListResponse])
def get_posts(board_id: int, db: Session = Depends(get_db)):
    """특정 게시판의 게시글 목록 조회 - 누구나 가능"""
    return get_board_posts(db, board_id)
