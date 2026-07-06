import datetime
from sqlalchemy import Column, String, Float, DateTime
from .base import Base

class ActionLog(Base):
    __tablename__ = "action_logs"
    
    id = Column(String, primary_key=True)
    agent_id = Column(String)
    action_type = Column(String)
    input_summary = Column(String)
    output_summary = Column(String)
    model_used = Column(String, nullable=True)
    model_provider = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    duration_ms = Column(Float, nullable=True)
