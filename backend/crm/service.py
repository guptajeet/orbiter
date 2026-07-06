import uuid
import datetime
from backend.core.database import SessionLocal
from backend.crm.models import RecruiterContact, Conversation
from .scoring import crm_scorer

class CRMService:
    def add_contact(self, email: str, name: str, source: str, **kwargs):
        db = SessionLocal()
        try:
            contact = db.query(RecruiterContact).filter(RecruiterContact.email == email).first()
            if not contact:
                contact = RecruiterContact(
                    id=str(uuid.uuid4()),
                    email=email,
                    name=name,
                    source=source,
                    **kwargs
                )
                db.add(contact)
            db.commit()
            return contact.id
        finally:
            db.close()

    def log_interaction(self, email: str, direction: str, content: str, thread_id: str = None, timestamp: str = None):
        db = SessionLocal()
        try:
            contact = db.query(RecruiterContact).filter(RecruiterContact.email == email).first()
            if not contact:
                return None
                
            contact.last_interaction_at = datetime.datetime.utcnow()
            
            # Find or create conversation
            convo = None
            if thread_id:
                convo = db.query(Conversation).filter(Conversation.thread_id == thread_id).first()
                
            if not convo:
                convo = db.query(Conversation).filter(
                    Conversation.contact_id == contact.id,
                    Conversation.status == "active"
                ).first()

            if not convo:
                convo = Conversation(
                    id=str(uuid.uuid4()),
                    contact_id=contact.id,
                    thread_id=thread_id,
                    status="active"
                )
                db.add(convo)
            
            from sqlalchemy.orm.attributes import flag_modified
            messages = list(convo.messages or [])
            messages.append({
                "direction": direction,
                "content": content,
                "timestamp": timestamp or datetime.datetime.utcnow().isoformat()
            })
            convo.messages = messages
            flag_modified(convo, "messages")
            
            # Recompute score
            contact.relationship_score = crm_scorer.compute_score(contact, db)
            
            db.commit()
        finally:
            db.close()

crm_service = CRMService()
