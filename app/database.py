from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 연결 정보 (SQLite 사용 예시)
SQLALCHEMY_DATABASE_URL = "sqlite:///./team_board.db"

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 (모든 모델이 상속받음)
Base = declarative_base()


# DB 세션 가져오기용 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
