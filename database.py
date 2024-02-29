from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:fsdbsdmsd@localhost/school"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
Base = declarative_base()