from fastapi import FastAPI

from app.routes.users import router as user_router

app = FastAPI()

# 라우터 등록
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Team Board API"}
