
# src/common/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Global placeholders
engine = None
SessionLocal = None
Base = declarative_base()


def init_engine(database_url: str):
    """
    Initialize the SQLAlchemy engine and session factory.
    Call this once at startup with your DATABASE_URL.
    """
    global engine, SessionLocal
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_engine():
    """Return the global engine object."""
    return engine


def get_db() -> Generator:
    """Provide a database session (dependency for FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
