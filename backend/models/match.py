import datetime
from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from .base import Base

class MatchResult(Base):
    __tablename__ = "match_results"
    
    id = Column(String, primary_key=True)
    resume_id = Column(String, ForeignKey("resume_profiles.id"))
    job_id = Column(String, ForeignKey("job_listings.id"))
    cosine_similarity = Column(Float)
    domain_fidelity_score = Column(Float)
    skill_overlap_pct = Column(Float)
    confidence_tier = Column(String)  # high | medium | low | no-fit
    scenario_classification = Column(String)
    tailoring_suggestions = Column(JSON, default=list)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
