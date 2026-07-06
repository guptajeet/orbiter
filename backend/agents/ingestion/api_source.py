import logging
import uuid
import datetime
from backend.agents.base import BaseAgent
from backend.plugins.registry import registry
from backend.models.job import JobListing
from backend.core.database import SessionLocal

logger = logging.getLogger(__name__)

class ApiSourceAgent(BaseAgent):
    def __init__(self):
        super().__init__("api_source")

    def process(self, task: dict):
        if task.get("type") != "discover_jobs":
            return {"status": "ignored"}
            
        filters = task.get("filters", {})
        results = []
        
        # Iterate over all registered source plugins
        for source_name, source_plugin_class in registry.sources.items():
            try:
                plugin = source_plugin_class()
                logger.info(f"Searching jobs using source: {source_name}")
                
                jobs = plugin.search_jobs(filters)
                
                # Save to database
                db = SessionLocal()
                new_jobs_count = 0
                for job_data in jobs:
                    # Very simple dedup hash for MVP
                    dedup_hash = f"{source_name}_{job_data.get('external_id')}"
                    
                    existing = db.query(JobListing).filter(JobListing.dedup_hash == dedup_hash).first()
                    if not existing:
                        job = JobListing(
                            id=str(uuid.uuid4()),
                            source_type="api",
                            source_name=source_name,
                            external_id=job_data.get("external_id"),
                            url=job_data.get("url"),
                            company_name=job_data.get("company_name"),
                            title=job_data.get("title"),
                            location=job_data.get("location"),
                            description_raw=job_data.get("description"),
                            dedup_hash=dedup_hash
                        )
                        db.add(job)
                        new_jobs_count += 1
                        
                        # Emit event for match engine
                        self.event_bus.publish("jobs", "new_job_found", {"job_id": job.id})
                        
                        # Queue match scoring task directly via Celery
                        try:
                            from backend.models.resume import ResumeProfile
                            from backend.tasks.intelligence_tasks import run_match_scoring
                            primary_resume = db.query(ResumeProfile).filter(ResumeProfile.is_primary == True).first()
                            if primary_resume:
                                run_match_scoring.delay(job.id, primary_resume.id)
                        except Exception as e:
                            logger.error(f"Failed to queue match scoring task for job {job.id}: {e}")
                        
                db.commit()
                db.close()
                
                results.append({
                    "source": source_name,
                    "found": len(jobs),
                    "new": new_jobs_count
                })
                
            except Exception as e:
                logger.error(f"Source plugin {source_name} failed: {e}")
                results.append({
                    "source": source_name,
                    "error": str(e)
                })
                
        return {"status": "success", "summary": results}

api_source_agent = ApiSourceAgent()
