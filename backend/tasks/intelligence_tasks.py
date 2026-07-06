from celery import shared_task
from backend.agents.intelligence.match_engine import match_engine_agent
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_match_scoring(self, job_id: str, resume_id: str):
    try:
        res = match_engine_agent.process({
            "type": "match_job",
            "job_id": job_id,
            "resume_id": resume_id,
        })
    except Exception as e:
        logger.error(f"run_match_scoring agent call failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
    
    if res and res.get("status") == "success":
        match_id = res.get("match_id")
        score = res.get("score", 0.0)
        
        import uuid
        import datetime
        from backend.core.database import SessionLocal
        from backend.core.automation_mode import mode_engine
        from backend.models.application import Application
        from backend.models.job import JobListing
        from backend.models.match import MatchResult
        from backend.core.action_logger import action_logger
        from backend.tasks.composition_tasks import run_resume_tailoring, run_cover_letter_generation
        
        db = SessionLocal()
        try:
            match = db.query(MatchResult).filter(MatchResult.id == match_id).first()
            if match:
                threshold = mode_engine.get_threshold()
                mode = mode_engine.global_mode
                
                if mode in ["copilot", "autopilot"] and score >= threshold:
                    existing_app = db.query(Application).filter(Application.match_id == match_id).first()
                    if not existing_app:
                        job = db.query(JobListing).filter(JobListing.id == match.job_id).first()
                        sub_method = "api" if job and job.source_type == "api" else "manual"
                        
                        from backend.models.resume import ResumeProfile
                        resume = db.query(ResumeProfile).filter(ResumeProfile.id == match.resume_id).first()
                        user_id = resume.user_id if resume else "default_user"
                        
                        app = Application(
                            id=str(uuid.uuid4()),
                            match_id=match_id,
                            user_id=user_id,
                            status="pending_approval",
                            submission_method=sub_method,
                            submitted_at=None,
                            status_updated_at=datetime.datetime.utcnow(),
                            tailored_resume_snapshot=None,
                            cover_letter_snapshot=None,
                            tracking_events=[],
                            source_url=job.url if job else None,
                        )
                        db.add(app)
                        db.commit()
                        
                        action_logger.log(
                            "autopipeline",
                            "application_created",
                            f"Job: {job.title if job else ''} ({score})",
                            f"Auto-created application {app.id[:8]} in mode '{mode}'"
                        )
                        
                        run_resume_tailoring.delay(match_id)
                        run_cover_letter_generation.delay(match_id)
        except Exception as e:
            db.rollback()
            logger.error(f"Error in run_match_scoring post-processing: {e}")
        finally:
            db.close()
            
    return res


@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_classification(self, job_id: str):
    from backend.agents.intelligence.classifier import classifier_agent
    try:
        return classifier_agent.process({"type": "classify_job", "job_id": job_id})
    except Exception as e:
        logger.error(f"run_classification failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}


@shared_task(bind=True, max_retries=3, soft_time_limit=120, time_limit=180)
def run_qa_verification(self, application_id: str):
    from backend.agents.intelligence.qa_agent import qa_agent
    try:
        return qa_agent.process({"type": "verify_application", "application_id": application_id})
    except Exception as e:
        logger.error(f"run_qa_verification failed: {e}")
        try:
            self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
        except self.MaxRetriesReachedError:
            return {"status": "error", "message": str(e), "retries_exhausted": True}
