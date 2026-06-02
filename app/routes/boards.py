from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import COMMON_RESPONSES, NOT_FOUND_RESPONSE
from app.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.user import User
from app.schemas.board import (
    BoardBaseResponse,
    BoardCreate,
    BoardListBaseResponse,
    BoardResponse,
    BoardUpdate,
)
from app.schemas.post import PostListBaseResponse, PostListResponse
from app.services.board_service import (
    create_board,
    delete_board,
    get_board,
    get_board_posts,
    get_boards,
    update_board,
)

router = APIRouter(prefix="/boards", tags=["게시판"])


@router.post(
    "/",
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


@router.get("/", response_model=BoardListBaseResponse, summary="게시판 목록 조회")
def get_list(db: Session = Depends(get_db)):
    """게시판 목록 조회 - 누구나 가능"""
    boards = get_boards(db)
    return BoardListBaseResponse(
        data=[BoardResponse.model_validate(board) for board in boards],
        message="게시판 목록 조회 성공",
    )


@router.get(
    "/{board_id}",
    response_model=BoardBaseResponse,
    summary="게시판 상세 조회",
    responses=NOT_FOUND_RESPONSE,
)
def get_detail(board_id: int, db: Session = Depends(get_db)):
    """게시판 상세 조회 - 누구나 가능"""
    board = get_board(db, board_id)
    return BoardBaseResponse(
        data=BoardResponse.model_validate(board),
        message="게시판 상세 조회 성공",
    )


@router.patch(
    "/{board_id}",
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
    "/{board_id}",
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


@router.get(
    "/{board_id}/posts",
    response_model=PostListBaseResponse,
    summary="게시판 게시글 목록 조회",
    responses=NOT_FOUND_RESPONSE,
)
def get_posts(board_id: int, db: Session = Depends(get_db)):
    """특정 게시판의 게시글 목록 조회 - 누구나 가능"""
    posts = get_board_posts(db, board_id)
    return PostListBaseResponse(
        data=[PostListResponse.model_validate(post) for post in posts],
        message="게시판 게시글 목록 조회 성공",
    )
