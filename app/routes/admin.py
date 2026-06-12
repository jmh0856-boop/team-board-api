from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import COMMON_RESPONSES
from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.board import (
    BoardBaseResponse,
    BoardCreate,
    BoardResponse,
    BoardUpdate,
)
from app.services.board_service import create_board, delete_board, update_board

router = APIRouter(prefix="/admin", tags=["관리자"])


@router.post(
    "/boards/",
    response_model=BoardBaseResponse,
    summary="게시판 생성",
    responses=COMMON_RESPONSES,
)
def create(
    board_data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """게시판 생성 - 관리자만 가능"""
    board = create_board(db, board_data)
    return BoardBaseResponse(
        data=BoardResponse.model_validate(board),
        message="게시판 생성 성공",
    )


@router.patch(
    "/boards/{board_id}",
    response_model=BoardBaseResponse,
    summary="게시판 수정",
    responses=COMMON_RESPONSES,
)
def update(
    board_id: int,
    board_data: BoardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """게시판 수정 - 관리자만 가능"""
    board = update_board(db, board_id, board_data)
    return BoardBaseResponse(
        data=BoardResponse.model_validate(board),
        message="게시판 수정 성공",
    )


@router.delete(
    "/boards/{board_id}",
    response_model=BoardBaseResponse,
    summary="게시판 삭제",
    responses=COMMON_RESPONSES,
)
def delete(
    board_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """게시판 삭제 - 관리자만 가능"""
    delete_board(db, board_id)
    return BoardBaseResponse(message="게시판 삭제 성공")
