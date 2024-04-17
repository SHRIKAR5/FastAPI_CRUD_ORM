from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB}'
# DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3306/employment_management_orm'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()