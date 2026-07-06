import datetime
from sqlalchemy import Column, String, JSON, DateTime
from .base import Base

class JobListing(Base):
    __tablename__ = "job_listings"
    
    id = Column(String, primary_key=True)
    source_type = Column(String)  # api | scraped | email | browser
    source_name = Column(String)
    external_id = Column(String)
    url = Column(String)
    company_name = Column(String)
    title = Column(String)
    location = Column(String)
    salary_range = Column(String, nullable=True)
    description_raw = Column(String)
    description_clean = Column(String)
    domain_tags = Column(JSON, default=list)
    industry_tags = Column(JSON, default=list)
    required_skills = Column(JSON, default=list)
    first_seen_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_refreshed_at = Column(DateTime, default=datetime.datetime.utcnow)
    dedup_hash = Column(String, unique=True, index=True)
