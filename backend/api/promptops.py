from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.promptops.models import PromptVersion
from backend.promptops.manager import prompt_manager

router = APIRouter(prefix="/api", tags=["promptops"])


class PromptCreate(BaseModel):
    prompt_name: str
    content: str
    variables: list[str] = []
    author: str = "system"


@router.get("/promptops/prompts")
def list_prompts(db: Session = Depends(get_db)):
    prompts = db.query(PromptVersion).order_by(PromptVersion.prompt_name, PromptVersion.version.desc()).all()

    grouped: dict = {}
    for p in prompts:
        if p.prompt_name not in grouped:
            grouped[p.prompt_name] = []
        grouped[p.prompt_name].append({
            "id": p.id,
            "version": p.version,
            "content": p.content,
            "variables": p.variables,
            "author": p.author,
            "is_active": p.is_active,
            "performance_metrics": p.performance_metrics,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })

    return {"prompts": grouped}


@router.post("/promptops/prompts")
def create_prompt_version(payload: PromptCreate):
    version_id = prompt_manager.create_version(
        prompt_name=payload.prompt_name,
        content=payload.content,
        variables=payload.variables,
        author=payload.author,
    )
    return {"status": "success", "version_id": version_id}


@router.post("/promptops/prompts/{prompt_name}/activate/{version_id}")
def activate_version(prompt_name: str, version_id: str, db: Session = Depends(get_db)):
    version = db.query(PromptVersion).filter(PromptVersion.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    prompt_manager.activate_version(prompt_name, version_id)
    return {"status": "activated", "prompt_name": prompt_name, "version_id": version_id}


@router.post("/promptops/prompts/{prompt_name}/rollback")
def rollback_prompt(prompt_name: str, db: Session = Depends(get_db)):
    versions = (
        db.query(PromptVersion)
        .filter(PromptVersion.prompt_name == prompt_name)
        .order_by(PromptVersion.version.desc())
        .all()
    )
    if len(versions) < 2:
        raise HTTPException(status_code=400, detail="Not enough versions to rollback")

    previous = versions[1]
    prompt_manager.activate_version(prompt_name, previous.id)
    return {"status": "rolled_back", "prompt_name": prompt_name, "activated_version": previous.version}
