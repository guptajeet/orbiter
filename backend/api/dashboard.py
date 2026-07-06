from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.job import JobListing
from backend.models.application import Application
from backend.models.match import MatchResult
from backend.models.action_log import ActionLog

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard/metrics")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    total_jobs = db.query(func.count(JobListing.id)).scalar() or 0
    total_applications = db.query(func.count(Application.id)).scalar() or 0
    pending_review = db.query(func.count(Application.id)).filter(Application.status == "pending_approval").scalar() or 0
    submitted = db.query(func.count(Application.id)).filter(Application.status == "submitted").scalar() or 0
    interviews = db.query(func.count(Application.id)).filter(Application.status == "interview").scalar() or 0
    total_matches = db.query(func.count(MatchResult.id)).scalar() or 0
    high_confidence = db.query(func.count(MatchResult.id)).filter(MatchResult.confidence_tier == "high").scalar() or 0

    redis_status = "offline"
    celery_status = "offline"
    email_status = "offline"
    
    # Check Redis
    import redis
    import os
    from backend.core.config import settings
    redis_url = settings.default_config.get("system", {}).get("redis_url", "redis://localhost:6379/0")
    try:
        r = redis.Redis.from_url(redis_url, socket_connect_timeout=1)
        r.ping()
        redis_status = "online"
    except Exception:
        pass
        
    # Check Celery
    if redis_status == "online":
        try:
            from backend.tasks.celery_app import celery_app
            insp = celery_app.control.inspect(timeout=0.5)
            stats = insp.stats()
            if stats:
                celery_status = "online"
        except Exception:
            pass
            
    # Check Email Monitor
    if os.path.exists("token.json"):
        email_status = "online"

    return {
        "new_matches": total_matches,
        "auto_applied": submitted,
        "review_needed": pending_review,
        "interviews": interviews,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "high_confidence_matches": high_confidence,
        "agent_status": {
            "master": "online",
            "match_engine": celery_status,
            "resume_tailor": celery_status,
            "email_monitor": email_status,
            "master_orchestrator": "online",
            "redis_event_bus": redis_status,
            "celery_workers": celery_status,
            "gmail_monitor": email_status,
        },
    }


@router.get("/dashboard/activity")
def get_activity(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    logs = (
        db.query(ActionLog)
        .order_by(ActionLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {
        "activity": [
            {
                "id": log.id,
                "agent_id": log.agent_id,
                "action_type": log.action_type,
                "input_summary": log.input_summary,
                "output_summary": log.output_summary,
                "model_used": log.model_used,
                "confidence_score": log.confidence_score,
                "duration_ms": log.duration_ms,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ]
    }
