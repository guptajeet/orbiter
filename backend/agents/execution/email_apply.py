import logging
from backend.agents.base import BaseAgent
from backend.plugins.registry import registry

logger = logging.getLogger(__name__)

class EmailApplyAgent(BaseAgent):
    def __init__(self):
        super().__init__("email_apply")

    def process(self, task: dict):
        if task.get("type") != "email_application":
            return {"status": "ignored"}
            
        contact = task.get("contact")  # email, name
        message = task.get("message")  # subject, body, html
        
        gmail_plugin_class = registry.get_channel("gmail")
        if not gmail_plugin_class:
            return {"status": "error", "message": "Gmail plugin not found"}
            
        try:
            plugin = gmail_plugin_class()
            # Check automation mode
            result = self.safe_execute("outreach", plugin.send_message, contact, message)
            return result
        except Exception as e:
            logger.error(f"Email apply agent failed: {e}")
            return {"status": "error", "message": str(e)}

email_apply_agent = EmailApplyAgent()
