from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User  # noqa: F401
from app.routes.auth import router as auth_router
from app.routes.users import router as user_router

# 앱 시작 시 DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Team Board API"}
