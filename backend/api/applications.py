from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import io

from backend.core.database import get_db
from backend.evaluation.tracker import metrics_tracker
from backend.models.application import Application
from backend.models.match import MatchResult
from backend.utils.exporter import generate_pdf_from_md, generate_docx_from_md

router = APIRouter(prefix="/api", tags=["applications"])


@router.get("/applications")
def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Application)
    if status:
        query = query.filter(Application.status == status)

    total = query.count()
    apps = query.order_by(Application.status_updated_at.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "applications": [
            {
                "id": a.id,
                "match_id": a.match_id,
                "user_id": a.user_id,
                "status": a.status,
                "submission_method": a.submission_method,
                "submitted_at": a.submitted_at.isoformat() if a.submitted_at else None,
                "status_updated_at": a.status_updated_at.isoformat() if a.status_updated_at else None,
                "source_url": a.source_url,
            }
            for a in apps
        ],
    }


@router.get("/applications/{app_id}")
def get_application(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {
        "id": app.id,
        "match_id": app.match_id,
        "user_id": app.user_id,
        "status": app.status,
        "submission_method": app.submission_method,
        "submitted_at": app.submitted_at.isoformat() if app.submitted_at else None,
        "status_updated_at": app.status_updated_at.isoformat() if app.status_updated_at else None,
        "tailored_resume_snapshot": app.tailored_resume_snapshot,
        "tailored_resume": app.tailored_resume_snapshot,  # Frontend alias
        "cover_letter_snapshot": app.cover_letter_snapshot,
        "cover_letter": app.cover_letter_snapshot,  # Frontend alias
        "tracking_events": app.tracking_events,
        "source_url": app.source_url,
    }


@router.post("/applications/{app_id}/approve")
def approve_application(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.status != "pending_approval":
        raise HTTPException(status_code=400, detail=f"Cannot approve application in '{app.status}' status")
    
    match = db.query(MatchResult).filter(MatchResult.id == app.match_id).first()
    job_id = match.job_id if match else None

    app.status = "submitted"
    db.commit()
    metrics_tracker.record_metric("application_approved", 1.0, {"application_id": app_id, "job_id": job_id})
    return {"status": "approved", "application_id": app.id}


@router.post("/applications/{app_id}/reject")
def reject_application(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.status != "pending_approval":
        raise HTTPException(status_code=400, detail=f"Cannot reject application in '{app.status}' status")
    
    match = db.query(MatchResult).filter(MatchResult.id == app.match_id).first()
    job_id = match.job_id if match else None

    app.status = "rejected"
    db.commit()
    metrics_tracker.record_metric("application_rejected", 0.0, {"application_id": app_id, "job_id": job_id})
    return {"status": "rejected", "application_id": app.id}


@router.get("/applications/{app_id}/export")
def export_document(
    app_id: str,
    type: str = Query("resume", enum=["resume", "cover_letter"]),
    format: str = Query("pdf", enum=["pdf", "docx", "txt", "md"]),
    db: Session = Depends(get_db)
):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    text_content = app.tailored_resume_snapshot if type == "resume" else app.cover_letter_snapshot
    if not text_content:
        raise HTTPException(status_code=400, detail=f"No {type} content available to export")
        
    filename = f"{type}_{app_id[:8]}"
    
    if format == "pdf":
        pdf_buf = generate_pdf_from_md(text_content)
        return StreamingResponse(
            pdf_buf,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'}
        )
    elif format == "docx":
        docx_buf = generate_docx_from_md(text_content)
        return StreamingResponse(
            docx_buf,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{filename}.docx"'}
        )
    elif format == "txt":
        txt_buf = io.BytesIO(text_content.encode("utf-8"))
        return StreamingResponse(
            txt_buf,
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{filename}.txt"'}
        )
    else:  # md
        md_buf = io.BytesIO(text_content.encode("utf-8"))
        return StreamingResponse(
            md_buf,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{filename}.md"'}
        )
