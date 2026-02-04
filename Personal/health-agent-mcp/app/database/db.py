from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base
from app.config import get_settings
from typing import Generator
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=settings.debug
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database - create all tables."""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
