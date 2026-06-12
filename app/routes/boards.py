import math

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import NOT_FOUND_RESPONSE
from app.database import get_db
from app.schemas.board import (
    BoardBaseResponse,
    BoardListBaseResponse,
    BoardResponse,
)
from app.schemas.post import PostListBaseResponse, PostListResponse
from app.services.board_service import get_board, get_boards
from app.services.post_service import get_posts as get_post_list

router = APIRouter(prefix="/boards", tags=["게시판"])


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


@router.get(
    "/{board_id}/posts",
    response_model=PostListBaseResponse,
    summary="게시판 게시글 목록 조회",
    responses=NOT_FOUND_RESPONSE,
)
def get_posts(
    board_id: int,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    """특정 게시판의 게시글 목록 조회 - 누구나 가능"""
    posts, total = get_post_list(db, board_id=board_id, page=page, size=size)
    return PostListBaseResponse(
        data=[PostListResponse.model_validate(post) for post in posts],
        total=total,
        page=page,
        size=size,
        total_pages=math.ceil(total / size) if size > 0 else 0,
        message="게시판 게시글 목록 조회 성공",
    )
