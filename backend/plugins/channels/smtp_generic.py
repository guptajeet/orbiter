from backend.plugins.base import BaseChannelPlugin
from backend.plugins.registry import registry
import os
import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

class SmtpChannelPlugin(BaseChannelPlugin):
    name = "smtp_generic"

    def __init__(self):
        self.server = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_message(self, contact: dict, message: dict) -> dict:
        recipient = contact.get("email")
        if not recipient:
            return {"status": "error", "message": "Recipient email not provided"}

        if not self.server or not self.username or not self.password:
            logger.warning("SMTP server credentials not configured. Simulating mock SMTP delivery.")
            return {"status": "success", "message_id": "smtp_mock_msg_777"}

        subject = message.get("subject", "Application Outreach")
        body = message.get("body", "")

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = recipient

        try:
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return {"status": "success", "message_id": "smtp_msg_" + str(hash(body))}
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            return {"status": "error", "message": str(e)}

    def check_responses(self) -> list:
        # SMTP is outbound-only by default; IMAP could parse incoming mail
        return []

# Register
registry.register_channel(SmtpChannelPlugin)
