import logging
from backend.agents.base import BaseAgent
from backend.services.email_service import email_service

logger = logging.getLogger(__name__)

class EmailMonitorAgent(BaseAgent):
    def __init__(self):
        super().__init__("email_monitor")

    def process(self, task: dict):
        if task.get("type") != "check_inbox":
            return {"status": "ignored"}
            
        from backend.core.database import SessionLocal
        from backend.crm.models import RecruiterContact, Conversation
        from backend.crm.service import crm_service

        db = SessionLocal()
        try:
            logger.info("Email monitor agent checking inbox...")
            
            contacts = db.query(RecruiterContact).all()
            if contacts:
                from_filters = [f"from:{c.email}" for c in contacts if c.email]
                query = f"({' OR '.join(from_filters)})"
            else:
                query = "is:unread"
                
            logger.info(f"Targeted search query: {query}")
            emails = email_service.get_recent_emails(query=query, max_results=20)
            for email in emails:
                sender_email = email.get("sender_email")
                snippet = email.get("snippet")
                thread_id = email.get("thread_id")
                
                logger.info(f"Email monitor found sender: {sender_email}")
                
                # Check if sender matches any CRM recruiter contact
                contact = db.query(RecruiterContact).filter(RecruiterContact.email == sender_email).first()
                if contact:
                    # Look up if conversation already has this message logged
                    convo = db.query(Conversation).filter(Conversation.contact_id == contact.id).first()
                    already_logged = False
                    if convo and convo.messages:
                        for msg in convo.messages:
                            if msg.get("content") == snippet:
                                already_logged = True
                                break
                                
                    if not already_logged:
                        logger.info(f"Logging matched inbound email from recruiter {sender_email}")
                        crm_service.log_interaction(
                            email=sender_email,
                            direction="inbound",
                            content=snippet,
                            thread_id=thread_id,
                            timestamp=email.get("timestamp")
                        )
                
                # Check for urgent items to trigger Alert Agent
                if "interview" in (snippet or "").lower():
                    self.event_bus.publish("reporting", "urgent_alert", {
                        "alert_type": "interview_invite",
                        "email_id": email.get('id'),
                        "snippet": snippet
                    })
                    
            return {"status": "success", "emails_processed": len(emails)}
        except Exception as e:
            logger.error(f"Email monitor agent failed: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            db.close()

email_monitor_agent = EmailMonitorAgent()
