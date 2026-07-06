import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.action_logger import action_logger
from backend.core.database import get_db
from backend.models.job import JobListing
from backend.models.application import Application
from backend.models.user import UserProfile
from backend.models.resume import ResumeProfile
from backend.models.match import MatchResult

router = APIRouter(prefix="/api", tags=["jobs"])


@router.get("/jobs")
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    company: Optional[str] = None,
    location: Optional[str] = None,
    source_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(JobListing)
    if company:
        query = query.filter(JobListing.company_name.ilike(f"%{company}%"))
    if location:
        query = query.filter(JobListing.location.ilike(f"%{location}%"))
    if source_type:
        query = query.filter(JobListing.source_type == source_type)

    total = query.count()
    jobs = query.order_by(JobListing.first_seen_at.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "jobs": [
            {
                "id": j.id,
                "source_type": j.source_type,
                "source_name": j.source_name,
                "company_name": j.company_name,
                "title": j.title,
                "location": j.location,
                "salary_range": j.salary_range,
                "url": j.url,
                "domain_tags": j.domain_tags,
                "required_skills": j.required_skills,
                "first_seen_at": j.first_seen_at.isoformat() if j.first_seen_at else None,
            }
            for j in jobs
        ],
    }


@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "source_type": job.source_type,
        "source_name": job.source_name,
        "external_id": job.external_id,
        "url": job.url,
        "company_name": job.company_name,
        "title": job.title,
        "location": job.location,
        "salary_range": job.salary_range,
        "description_raw": job.description_raw,
        "description_clean": job.description_clean,
        "domain_tags": job.domain_tags,
        "industry_tags": job.industry_tags,
        "required_skills": job.required_skills,
        "first_seen_at": job.first_seen_at.isoformat() if job.first_seen_at else None,
        "last_refreshed_at": job.last_refreshed_at.isoformat() if job.last_refreshed_at else None,
    }


@router.post("/jobs/discover")
def trigger_job_discovery():
    import threading
    from backend.agents.ingestion.supervisor import ingestion_supervisor
    threading.Thread(target=ingestion_supervisor.trigger_discovery, daemon=True).start()
    action_logger.log("ingestion", "job_discovery", "Discovery triggered", "Background discovery started")
    return {"status": "discovery_triggered"}


@router.post("/jobs/{job_id}/apply")
def apply_to_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobListing).filter(JobListing.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    user = db.query(UserProfile).first()
    if not user:
        user = UserProfile(id=str(uuid.uuid4()), email_accounts=[], preferences={}, automation_config={})
        db.add(user)
        db.flush()

    resume = db.query(ResumeProfile).filter(ResumeProfile.user_id == user.id).first()
    if not resume:
        resume = db.query(ResumeProfile).filter(ResumeProfile.is_primary == True).first()
    if not resume:
        resume = db.query(ResumeProfile).first()

    match = MatchResult(
        id=str(uuid.uuid4()),
        resume_id=resume.id if resume else None,
        job_id=job.id,
        cosine_similarity=0.0,
        domain_fidelity_score=0.0,
        skill_overlap_pct=0.0,
        confidence_tier="manual",
        scenario_classification="manual_apply",
        tailoring_suggestions=[],
        generated_at=datetime.datetime.utcnow(),
    )
    db.add(match)
    db.flush()

    application = Application(
        id=str(uuid.uuid4()),
        match_id=match.id,
        user_id=user.id,
        status="pending_approval",
        submission_method="manual",
        submitted_at=None,
        status_updated_at=datetime.datetime.utcnow(),
        tailored_resume_snapshot=None,
        cover_letter_snapshot=None,
        tracking_events=[],
        source_url=job.url,
    )
    db.add(application)
    db.commit()

    # Trigger composition tasks in Celery
    try:
        from backend.tasks.composition_tasks import run_resume_tailoring, run_cover_letter_generation
        run_resume_tailoring.delay(match.id)
        run_cover_letter_generation.delay(match.id)
    except Exception as e:
        action_logger.log("manual_apply", "celery_trigger_failed", f"Match: {match.id[:8]}", f"Error: {str(e)}")

    action_logger.log("manual_apply", "application_created", f"Job: {job.title} at {job.company_name}", f"Application {application.id[:8]} created")

    return {
        "status": "application_created",
        "application_id": application.id,
        "job_title": job.title,
        "company": job.company_name,
    }
