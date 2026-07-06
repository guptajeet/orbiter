import uuid
import io
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.database import get_db
from backend.models.user import UserProfile
from backend.models.resume import ResumeProfile
from backend.agents.intelligence.resume_parser import resume_parser_agent
from backend.core.action_logger import action_logger

router = APIRouter(prefix="/api", tags=["profile"])


def extract_text(content: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext == "pdf":
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            pass

    if ext == "docx":
        try:
            import docx
            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            pass

    return content.decode("utf-8", errors="ignore")


class ProfileCreate(BaseModel):
    email_accounts: list[str] = []
    linkedin_url: Optional[str] = None
    indeed_url: Optional[str] = None
    preferences: dict = {}
    automation_config: dict = {}


@router.get("/profile")
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(UserProfile).first()
    if not profile:
        return {
            "id": None,
            "email_accounts": [],
            "linkedin_url": None,
            "indeed_url": None,
            "preferences": {},
            "automation_config": {},
            "created_at": None,
            "updated_at": None,
        }
    return {
        "id": profile.id,
        "email_accounts": profile.email_accounts,
        "linkedin_url": profile.linkedin_url,
        "indeed_url": profile.indeed_url,
        "preferences": profile.preferences,
        "automation_config": profile.automation_config,
        "created_at": profile.created_at.isoformat() if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
    }


@router.post("/profile")
def create_or_update_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).first()
    if profile:
        profile.email_accounts = payload.email_accounts
        profile.linkedin_url = payload.linkedin_url
        profile.indeed_url = payload.indeed_url
        profile.preferences = payload.preferences
        profile.automation_config = payload.automation_config
    else:
        profile = UserProfile(
            id=str(uuid.uuid4()),
            email_accounts=payload.email_accounts,
            linkedin_url=payload.linkedin_url,
            indeed_url=payload.indeed_url,
            preferences=payload.preferences,
            automation_config=payload.automation_config,
        )
        db.add(profile)
        db.flush()
        db.query(ResumeProfile).filter(ResumeProfile.user_id == "default_user").update({"user_id": profile.id})
    db.commit()
    db.refresh(profile)
    action_logger.log("profile", "profile_updated", f"Emails: {len(payload.email_accounts)}", f"Profile {profile.id[:8]} saved")
    return {"status": "success", "profile_id": profile.id}


@router.post("/profile/resume")
async def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    text_content = extract_text(content, file.filename or "resume.txt")

    if not text_content or len(text_content.strip()) < 10:
        raise HTTPException(status_code=400, detail="Could not extract text from file. Ensure it is a valid PDF or DOCX.")

    profile = db.query(UserProfile).first()
    user_id = profile.id if profile else "default_user"

    resume = ResumeProfile(
        id=str(uuid.uuid4()),
        user_id=user_id,
        raw_text=text_content,
        is_primary=True,
    )
    db.add(resume)
    db.commit()

    background_tasks.add_task(
        resume_parser_agent.process,
        {"type": "parse_resume", "raw_text": text_content, "profile_id": resume.id},
    )

    action_logger.log("resume_parser", "resume_uploaded", f"File: {file.filename}", f"Extracted {len(text_content)} chars, parsing in background")

    return {"status": "success", "resume_id": resume.id, "text_length": len(text_content)}
