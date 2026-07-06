import datetime
from sqlalchemy import Column, String, JSON, DateTime, Boolean, ForeignKey
from .base import Base

class ResumeProfile(Base):
    __tablename__ = "resume_profiles"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_profiles.id"))
    label = Column(String)  # e.g., "backend-engineer"
    raw_text = Column(String)
    parsed_sections = Column(JSON, default=dict)
    # Note: the embedding vector will be stored in ChromaDB, not SQLite.
    domain_tags = Column(JSON, default=list)
    industry_tags = Column(JSON, default=list)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
