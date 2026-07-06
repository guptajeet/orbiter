import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.core.database import get_db
from backend.crm.models import RecruiterContact, Conversation
from backend.crm.service import crm_service

router = APIRouter(prefix="/api", tags=["crm"])


class ContactCreate(BaseModel):
    email: str
    name: str
    source: str
    company: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    notes: Optional[str] = None


class ConversationMessageCreate(BaseModel):
    content: str
    direction: str = "outbound"


@router.get("/crm/contacts")
def list_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    total = db.query(RecruiterContact).count()
    contacts = (
        db.query(RecruiterContact)
        .order_by(RecruiterContact.last_interaction_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "contacts": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "company": c.company,
                "title": c.title,
                "source": c.source,
                "relationship_score": c.relationship_score,
                "tags": c.tags,
                "last_interaction_at": c.last_interaction_at.isoformat() if c.last_interaction_at else None,
            }
            for c in contacts
        ],
    }


@router.post("/crm/contacts")
def add_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    contact_id = crm_service.add_contact(
        email=payload.email,
        name=payload.name,
        source=payload.source,
        company=payload.company,
        title=payload.title,
        phone=payload.phone,
        linkedin_url=payload.linkedin_url,
        notes=payload.notes,
    )
    return {"status": "success", "contact_id": contact_id}


@router.get("/crm/contacts/{contact_id}")
def get_contact(contact_id: str, db: Session = Depends(get_db)):
    contact = db.query(RecruiterContact).filter(RecruiterContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone": contact.phone,
        "linkedin_url": contact.linkedin_url,
        "company": contact.company,
        "title": contact.title,
        "department": contact.department,
        "source": contact.source,
        "relationship_score": contact.relationship_score,
        "tags": contact.tags,
        "notes": contact.notes,
        "first_contact_at": contact.first_contact_at.isoformat() if contact.first_contact_at else None,
        "last_interaction_at": contact.last_interaction_at.isoformat() if contact.last_interaction_at else None,
    }


@router.get("/crm/conversations/{contact_id}")
def get_conversations(contact_id: str, db: Session = Depends(get_db)):
    contact = db.query(RecruiterContact).filter(RecruiterContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    convos = db.query(Conversation).filter(Conversation.contact_id == contact_id).all()
    return {
        "contact_id": contact_id,
        "conversations": [
            {
                "id": c.id,
                "thread_id": c.thread_id,
                "status": c.status,
                "messages": c.messages,
                "next_followup_at": c.next_followup_at.isoformat() if c.next_followup_at else None,
            }
            for c in convos
        ],
    }


@router.post("/crm/conversations/{contact_id}/messages")
def log_conversation_message(contact_id: str, payload: ConversationMessageCreate, db: Session = Depends(get_db)):
    contact = db.query(RecruiterContact).filter(RecruiterContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    crm_service.log_interaction(
        email=contact.email,
        direction=payload.direction,
        content=payload.content,
    )
    return {"status": "success"}
