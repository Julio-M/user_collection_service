from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

SQLALCHEMY_DATABASE_URI = DATABASE_URL  # 1


if "sqlite" in DATABASE_URL:
    from sqlalchemy.pool import SingletonThreadPool

    db_engine = create_engine(DATABASE_URL, poolclass=SingletonThreadPool)
else:
    db_engine = create_engine(DATABASE_URL)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
