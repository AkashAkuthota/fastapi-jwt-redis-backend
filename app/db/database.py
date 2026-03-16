
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db_url = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    db_url,
    connect_args={"sslmode": "require"},
    pool_pre_ping=True,
    pool_recycle=300
)
session = sessionmaker(autoflush = False,autocommit = False,bind = engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()