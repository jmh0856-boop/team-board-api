# 1. 필요한 SQLAlchemy 도구들을 불러옵니다.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 2. 우리가 아까 만든 설정 객체(config)에서 DB 접속 주소를 가져옵니다.
from app.core.config import settings

# 3. 데이터베이스와 연결할 엔진을 생성합니다. (접속 정보를 활용)
engine = create_engine(settings.DATABASE_URL)

# 4. 세션 팩토리를 설정합니다. (각 요청마다 독립적인 세션을 생성하기 위함)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. 모든 모델이 상속받을 공통 기반(Base) 클래스를 만듭니다.
Base = declarative_base()
