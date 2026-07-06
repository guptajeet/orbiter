from backend.plugins.base import BaseChannelPlugin
from backend.plugins.registry import registry
from backend.services.email_service import email_service

class GmailChannelPlugin(BaseChannelPlugin):
    name = "gmail"
    
    def send_message(self, contact: dict, message: dict) -> dict:
        to = contact.get("email")
        subject = message.get("subject", "Hello")
        body = message.get("body", "")
        html = message.get("html", False)
        
        if not to:
            return {"status": "error", "message": "No email address provided"}
            
        return email_service.send_email(to, subject, body, html)

    def check_responses(self) -> list:
        return email_service.get_recent_emails()

# Register itself
registry.register_channel(GmailChannelPlugin)
