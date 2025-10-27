# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or "postgresql" in DATABASE_URL:
    # Fallback to SQLite for development
    DATABASE_URL = "sqlite:///./finance.db"
    logger.warning("Using SQLite database: finance.db")

try:
    # echo=True can help debug SQL statements
    engine = create_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info(f"Database connection established: {DATABASE_URL}")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise
