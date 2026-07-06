import datetime
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from .base import Base

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String, primary_key=True)
    match_id = Column(String, ForeignKey("match_results.id"))
    user_id = Column(String, ForeignKey("user_profiles.id"))
    status = Column(String)  # queued | composing | pending_approval | submitted | acknowledged | rejected | interview | offer
    submission_method = Column(String)  # api | browser | email | manual
    submitted_at = Column(DateTime, nullable=True)
    status_updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    tailored_resume_snapshot = Column(String, nullable=True)
    cover_letter_snapshot = Column(String, nullable=True)
    tracking_events = Column(JSON, default=list)
    source_url = Column(String, nullable=True)
