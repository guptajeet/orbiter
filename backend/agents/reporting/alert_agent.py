import logging
from backend.agents.base import BaseAgent
from backend.services.email_service import email_service

logger = logging.getLogger(__name__)

class AlertAgent(BaseAgent):
    def __init__(self):
        super().__init__("alert_agent")

    def process(self, task: dict):
        if task.get("type") != "urgent_alert":
            return {"status": "ignored"}
            
        alert_type = task.get("alert_type")
        snippet = task.get("snippet", "")
        
        logger.warning(f"URGENT ALERT triggered: {alert_type}")
        
        try:
            subject = f"🚨 Orbiter Alert: {alert_type.replace('_', ' ').title()}"
            body = f"An urgent event requires your attention:\n\n{snippet}\n\nPlease check the dashboard."
            
            email_service.send_email(
                to="me",
                subject=subject,
                body=body
            )
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Alert agent failed: {e}")
            return {"status": "error", "message": str(e)}

alert_agent = AlertAgent()
