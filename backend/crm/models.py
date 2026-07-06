import datetime
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, ForeignKey
from backend.models.base import Base

class RecruiterContact(Base):
    __tablename__ = "recruiter_contacts"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    company = Column(String, nullable=True)
    title = Column(String, nullable=True)
    department = Column(String, nullable=True)
    source = Column(String)
    relationship_score = Column(Float, default=0.0)
    tags = Column(JSON, default=list)
    notes = Column(String, nullable=True)
    first_contact_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_interaction_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Conversation(Base):
    __tablename__ = "crm_conversations"
    
    id = Column(String, primary_key=True)
    contact_id = Column(String, ForeignKey("recruiter_contacts.id"))
    application_id = Column(String, ForeignKey("applications.id"), nullable=True)
    thread_id = Column(String, nullable=True)
    messages = Column(JSON, default=list)
    status = Column(String)  # active | dormant | closed
    next_followup_at = Column(DateTime, nullable=True)

class FollowUpSchedule(Base):
    __tablename__ = "followup_schedules"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("crm_conversations.id"))
    contact_id = Column(String, ForeignKey("recruiter_contacts.id"))
    trigger_type = Column(String)  # time_based | event_based
    interval_hours = Column(Integer, default=72)
    max_followups = Column(Integer, default=3)
    current_count = Column(Integer, default=0)
    last_sent_at = Column(DateTime, nullable=True)
    status = Column(String)  # pending | sent | responded | exhausted
