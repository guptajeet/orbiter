import base64
import logging
from email.message import EmailMessage
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.creds = None
        self.service = None

    def _initialize(self):
        if self.service:
            return True

        token_path = "token.json"
        if not __import__("os").path.exists(token_path):
            logger.warning("token.json not found. Run 'python setup_gmail.py' to authenticate Gmail.")
            return False

        try:
            from google.oauth2.credentials import Credentials
            self.creds = Credentials.from_authorized_user_file(token_path, [
                'https://www.googleapis.com/auth/gmail.modify'
            ])
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True
        except Exception as e:
            logger.error(f"Gmail init failed: {e}")
            return False

    def send_email(self, to: str, subject: str, body: str, html: bool = False):
        if not self._initialize():
            return {"status": "error", "message": "Gmail not authenticated. Run 'python setup_gmail.py'"}

        message = EmailMessage()
        message.set_content(body)
        if html:
            message.add_alternative(body, subtype='html')

        message['To'] = to
        message['From'] = "me"
        message['Subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        try:
            send_message = self.service.users().messages().send(userId="me", body=create_message).execute()
            return {"status": "success", "message_id": send_message["id"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_recent_emails(self, query: str = "is:unread", max_results: int = 10):
        if not self._initialize():
            return []

        try:
            results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])

            parsed_messages = []
            for msg in messages:
                msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                
                headers = msg_data.get('payload', {}).get('headers', [])
                sender = ""
                subject = ""
                for h in headers:
                    name = h.get('name')
                    if name == 'From':
                        sender = h.get('value', '')
                    elif name == 'Subject':
                        subject = h.get('value', '')
                        
                import re
                email_match = re.search(r'<([^>]+)>', sender)
                sender_email = email_match.group(1).lower().strip() if email_match else sender.lower().strip()
                
                snippet = msg_data.get('snippet') or ""
                if not snippet.strip():
                    snippet = f"[Subject: {subject}]" if subject else "(No content)"
                    
                import datetime
                internal_date_ms = msg_data.get('internalDate')
                if internal_date_ms:
                    dt = datetime.datetime.utcfromtimestamp(int(internal_date_ms) / 1000.0)
                    timestamp_iso = dt.isoformat()
                else:
                    timestamp_iso = datetime.datetime.utcnow().isoformat()
                
                parsed_messages.append({
                    "id": msg['id'],
                    "snippet": snippet,
                    "sender_raw": sender,
                    "sender_email": sender_email,
                    "thread_id": msg_data.get('threadId'),
                    "timestamp": timestamp_iso
                })

            return parsed_messages
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []

email_service = EmailService()
