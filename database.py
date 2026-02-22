import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fallback to a local SQLite database if Docker isn't running so you can finish the assignment!
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# SQLite requires this connect_args flag
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency to get a database session.
    Yields a session and automatically closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
