import datetime
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime
from backend.models.base import Base

class AgentMemory(Base):
    __tablename__ = "agent_memories"
    
    id = Column(String, primary_key=True)
    agent_id = Column(String)
    memory_type = Column(String)
    content = Column(JSON)
    # The embedding is stored in ChromaDB, mapped by this ID
    relevance_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_accessed_at = Column(DateTime, default=datetime.datetime.utcnow)
    access_count = Column(Integer, default=0)
