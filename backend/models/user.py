import datetime
from sqlalchemy import Column, String, JSON, DateTime
from .base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True)
    email_accounts = Column(JSON, default=list)
    linkedin_url = Column(String, nullable=True)
    indeed_url = Column(String, nullable=True)
    preferences = Column(JSON, default=dict)
    automation_config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
