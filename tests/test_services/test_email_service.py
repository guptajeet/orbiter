import pytest
from unittest.mock import MagicMock, patch
from backend.services.email_service import EmailService

@pytest.fixture
def mock_gmail_service():
    mock_service = MagicMock()
    mock_users = MagicMock()
    mock_messages = MagicMock()
    
    mock_service.users.return_value = mock_users
    mock_users.messages.return_value = mock_messages
    
    return mock_service, mock_messages

def test_send_email_success(mock_gmail_service):
    mock_service, mock_messages = mock_gmail_service
    
    # Mock send message execute response
    mock_messages.send.return_value.execute.return_value = {"id": "msg123"}
    
    email_service = EmailService()
    
    with patch("os.path.exists", return_value=True):
        with patch("google.oauth2.credentials.Credentials.from_authorized_user_file", return_value=MagicMock()):
            with patch("backend.services.email_service.build", return_value=mock_service):
                result = email_service.send_email(
                    to="recruiter@example.com",
                    subject="Application Follow-up",
                    body="Hello, just checking in.",
                    html=True
                )
                
                assert result["status"] == "success"
                assert result["message_id"] == "msg123"
                mock_messages.send.assert_called_once()

def test_send_email_error(mock_gmail_service):
    mock_service, mock_messages = mock_gmail_service
    mock_messages.send.return_value.execute.side_effect = Exception("API error")
    
    email_service = EmailService()
    
    with patch("os.path.exists", return_value=True):
        with patch("google.oauth2.credentials.Credentials.from_authorized_user_file", return_value=MagicMock()):
            with patch("backend.services.email_service.build", return_value=mock_service):
                result = email_service.send_email(
                    to="recruiter@example.com",
                    subject="Application Follow-up",
                    body="Hello, just checking in."
                )
                
                assert result["status"] == "error"
                assert "API error" in result["message"]

def test_get_recent_emails(mock_gmail_service):
    mock_service, mock_messages = mock_gmail_service
    
    mock_messages.list.return_value.execute.return_value = {
        "messages": [{"id": "msg1"}, {"id": "msg2"}]
    }
    mock_messages.get.return_value.execute.side_effect = [
        {"id": "msg1", "snippet": "First unread message"},
        {"id": "msg2", "snippet": "Second unread message"}
    ]
    
    email_service = EmailService()
    
    with patch("os.path.exists", return_value=True):
        with patch("google.oauth2.credentials.Credentials.from_authorized_user_file", return_value=MagicMock()):
            with patch("backend.services.email_service.build", return_value=mock_service):
                emails = email_service.get_recent_emails(query="is:unread", max_results=5)
                
                assert len(emails) == 2
                assert emails[0]["id"] == "msg1"
                assert emails[0]["snippet"] == "First unread message"
                assert emails[1]["id"] == "msg2"
                assert emails[1]["snippet"] == "Second unread message"
                
                mock_messages.list.assert_called_once_with(userId="me", q="is:unread", maxResults=5)
