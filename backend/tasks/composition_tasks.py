from celery import shared_task
from backend.core.database import SessionLocal
from backend.models.match import MatchResult
from backend.models.resume import ResumeProfile
from backend.models.job import JobListing
from backend.models.application import Application
from backend.core.action_logger import action_logger
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_resume_tailoring(self, match_id: str):
    from backend.agents.composition.resume_tailor import resume_tailor_agent
    db = SessionLocal()
    try:
        match = db.query(MatchResult).filter(MatchResult.id == match_id).first()
        if not match:
            return {"status": "error", "message": "Match not found"}
        
        resume = db.query(ResumeProfile).filter(ResumeProfile.id == match.resume_id).first()
        job = db.query(JobListing).filter(JobListing.id == match.job_id).first()
        if not resume or not job:
            return {"status": "error", "message": "Resume or Job not found"}
        
        agent_result = resume_tailor_agent.process({
            "type": "tailor_resume",
            "resume_text": resume.raw_text,
            "job_description": job.description_raw
        })
        
        if agent_result.get("status") == "success":
            tailored_resume = agent_result.get("tailored_resume")
            app = db.query(Application).filter(Application.match_id == match_id).first()
            if app:
                app.tailored_resume_snapshot = tailored_resume
                db.commit()
                action_logger.log("resume_tailor", "resume_tailored", f"Match: {match_id[:8]}", f"Tailored resume saved")
                return {"status": "success", "message": "Resume tailored and saved"}
            else:
                return {"status": "error", "message": "Application not found for match"}
        return agent_result
    except Exception as e:
        logger.error(f"run_resume_tailoring failed: {e}")
        db.rollback()
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
    finally:
        db.close()


@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_cover_letter_generation(self, match_id: str):
    from backend.agents.composition.cover_letter import cover_letter_agent
    db = SessionLocal()
    try:
        match = db.query(MatchResult).filter(MatchResult.id == match_id).first()
        if not match:
            return {"status": "error", "message": "Match not found"}
        
        resume = db.query(ResumeProfile).filter(ResumeProfile.id == match.resume_id).first()
        job = db.query(JobListing).filter(JobListing.id == match.job_id).first()
        if not resume or not job:
            return {"status": "error", "message": "Resume or Job not found"}
        
        agent_result = cover_letter_agent.process({
            "type": "generate_cover_letter",
            "resume_text": resume.raw_text,
            "job_description": job.description_raw,
            "company_name": job.company_name
        })
        
        if agent_result.get("status") == "success":
            cover_letter = agent_result.get("cover_letter")
            app = db.query(Application).filter(Application.match_id == match_id).first()
            if app:
                app.cover_letter_snapshot = cover_letter
                db.commit()
                action_logger.log("cover_letter", "cover_letter_generated", f"Match: {match_id[:8]}", f"Cover letter saved")
                return {"status": "success", "message": "Cover letter generated and saved"}
            else:
                return {"status": "error", "message": "Application not found for match"}
        return agent_result
    except Exception as e:
        logger.error(f"run_cover_letter_generation failed: {e}")
        db.rollback()
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
    finally:
        db.close()
