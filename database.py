import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# We assume a standard PostgreSQL connection. Update credentials as needed.
# Format: postgresql://<username>:<password>@<host>:<port>/<dbname>
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/asset_management"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
