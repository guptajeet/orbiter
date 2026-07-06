import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Find absolute project root (orbiter/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATABASE_URL = settings.default_config.get("system", {}).get("database_url", "sqlite:///./orbiter.db")

# If it is a relative sqlite path, resolve it relative to project root
if DATABASE_URL.startswith("sqlite:///./"):
    db_filename = DATABASE_URL.replace("sqlite:///./", "")
    db_path = PROJECT_ROOT / db_filename
    DATABASE_URL = f"sqlite:///{db_path}"
elif DATABASE_URL.startswith("sqlite:///"):
    db_filename = DATABASE_URL.replace("sqlite:///", "")
    if not Path(db_filename).is_absolute():
        db_path = PROJECT_ROOT / db_filename
        DATABASE_URL = f"sqlite:///{db_path}"

# In SQLite, we need connect_args={"check_same_thread": False} to avoid thread issues with FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
