from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from authentication.core.config import DATABASE_URL


SQLALCHEMY_DATABASE_URI = DATABASE_URL  # 1


engine = create_engine(  # 2
    SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},  # 3
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 4