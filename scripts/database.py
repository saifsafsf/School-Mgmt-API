from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
Base = declarative_base()