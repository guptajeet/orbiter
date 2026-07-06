import datetime
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime, Boolean, ForeignKey
from backend.models.base import Base

class PromptVersion(Base):
    __tablename__ = "prompt_versions"
    
    id = Column(String, primary_key=True)
    prompt_name = Column(String)
    version = Column(Integer)
    content = Column(String)
    variables = Column(JSON, default=list)
    author = Column(String)
    is_active = Column(Boolean, default=False)
    performance_metrics = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PromptExperiment(Base):
    __tablename__ = "prompt_experiments"
    
    id = Column(String, primary_key=True)
    prompt_name = Column(String)
    control_version_id = Column(String, ForeignKey("prompt_versions.id"))
    treatment_version_id = Column(String, ForeignKey("prompt_versions.id"))
    traffic_split = Column(JSON, default={"control": 0.5, "treatment": 0.5})
    metric = Column(String)
    status = Column(String)  # draft | running | concluded
    results = Column(JSON, default=dict)
