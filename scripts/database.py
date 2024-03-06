from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import sys

sys.path.insert(0, "C:\\NUST\\Jobs\\Sila")

from config import settings

# MySQL connector link
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# used in models.py to define the schema of the db
Base = declarative_base()