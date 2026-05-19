from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 환경 변수 이름을 클래스 변수로 정의
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # .env 파일 경로 설정
    class Config:
        env_file = ".env"


# 전역 설정 객체 생성
settings = Settings()
