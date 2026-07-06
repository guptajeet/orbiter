import uuid
import hashlib
from backend.core.database import SessionLocal
from backend.models.job import JobListing

class JobService:
    def list_jobs(self, limit: int = 50, offset: int = 0, source: str = None, domain: str = None):
        db = SessionLocal()
        try:
            query = db.query(JobListing)
            if source:
                query = query.filter(JobListing.source_name == source)
            if domain:
                query = query.filter(JobListing.domain_tags.contains(domain))
            return query.order_by(JobListing.first_seen_at.desc()).offset(offset).limit(limit).all()
        finally:
            db.close()
    
    def get_job(self, job_id: str):
        db = SessionLocal()
        try:
            return db.query(JobListing).filter(JobListing.id == job_id).first()
        finally:
            db.close()
    
    def upsert_job(self, job_data: dict) -> str:
        db = SessionLocal()
        try:
            dedup_key = f"{job_data.get('title', '')}|{job_data.get('company_name', '')}|{job_data.get('url', '')}"
            dedup_hash = hashlib.sha256(dedup_key.encode()).hexdigest()
            
            existing = db.query(JobListing).filter(JobListing.dedup_hash == dedup_hash).first()
            if existing:
                return existing.id
            
            job = JobListing(
                id=str(uuid.uuid4()),
                dedup_hash=dedup_hash,
                **job_data
            )
            db.add(job)
            db.commit()
            return job.id
        finally:
            db.close()
    
    def get_count(self) -> int:
        db = SessionLocal()
        try:
            return db.query(JobListing).count()
        finally:
            db.close()

job_service = JobService()
