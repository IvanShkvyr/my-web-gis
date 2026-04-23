from dotenv import load_dotenv
from pathlib import Path
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


safe_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
safe_user = quote_plus(DB_USER) if DB_USER else ""

DATABASE_URL = (
    f"postgresql://{safe_user}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
               )
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
