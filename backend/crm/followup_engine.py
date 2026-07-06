import logging
import datetime
import uuid
from backend.core.database import SessionLocal
from backend.crm.models import FollowUpSchedule, Conversation, RecruiterContact
from backend.services.email_service import email_service

logger = logging.getLogger(__name__)

class FollowUpEngine:
    def schedule_followup(self, conversation_id: str, contact_id: str, hours: int = 72):
        db = SessionLocal()
        try:
            schedule = FollowUpSchedule(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                contact_id=contact_id,
                trigger_type="time_based",
                interval_hours=hours,
                status="pending"
            )
            db.add(schedule)
            db.commit()
            return schedule.id
        finally:
            db.close()

    def process_due_followups(self):
        db = SessionLocal()
        try:
            now = datetime.datetime.utcnow()
            due_schedules = db.query(FollowUpSchedule).filter(
                FollowUpSchedule.status == "pending"
            ).all()
            
            for schedule in due_schedules:
                convo = db.query(Conversation).filter(Conversation.id == schedule.conversation_id).first()
                if convo and convo.status == "active":
                    # Check if enough time has passed since last interaction
                    contact = db.query(RecruiterContact).filter(RecruiterContact.id == schedule.contact_id).first()
                    time_diff = now - contact.last_interaction_at
                    
                    if time_diff.total_seconds() >= schedule.interval_hours * 3600:
                        # Send follow up
                        self._execute_followup(schedule, contact, convo)
        finally:
            db.close()
            
    def _execute_followup(self, schedule, contact, convo):
        logger.info(f"Executing followup for {contact.email}")
        email_service.send_email(
            to=contact.email,
            subject="Following up on my application",
            body="Hi, just following up on my recent application..."
        )
        schedule.current_count += 1
        schedule.last_sent_at = datetime.datetime.utcnow()
        if schedule.current_count >= schedule.max_followups:
            schedule.status = "exhausted"

followup_engine = FollowUpEngine()
