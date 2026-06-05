from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.models import board  # noqa: F401
from app.models import comment  # noqa: F401
from app.models import comment_like  # noqa: F401
from app.models import like  # noqa: F401
from app.models import post  # noqa: F401
from app.models import tag  # noqa: F401
from app.models.user import User  # noqa: F401
from app.routes.auth import router as auth_router
from app.routes.boards import router as board_router
from app.routes.comments import router as comment_router
from app.routes.posts import router as post_router
from app.routes.tags import router as tag_router
from app.routes.users import router as user_router

# 앱 시작 시 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    swagger_ui_parameters={"persistAuthorization": True},
)


# 공통 에러 응답 형식 통일
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail},
    )


# 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(board_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(tag_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Team Board API"}
