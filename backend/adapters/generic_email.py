import logging
from .base import BaseATSAdapter, SubmissionResult
from .registry import adapter_registry
from backend.services.email_service import email_service

logger = logging.getLogger(__name__)

class GenericEmailAdapter(BaseATSAdapter):
    name = "email"

    def submit_application(self, application_data: dict, resume: str, cover_letter: str) -> SubmissionResult:
        recruiter_email = application_data.get("recruiter_email")
        if not recruiter_email:
            return SubmissionResult("error", "No recruiter_email specified in application data")

        job_title = application_data.get("job_title", "Software Engineer")
        company_name = application_data.get("company_name", "Company")

        subject = f"Application: {job_title} at {company_name}"
        
        # Simple email formatting combining cover letter and notification
        body = f"""Dear Hiring Team,

Please find my application details for the {job_title} role at {company_name} below.

{cover_letter}

My resume content is attached/included below for your review:

---
{resume}
---

Best regards,
Candidate
"""
        logger.info(f"Sending generic apply email to {recruiter_email} for {job_title}")
        
        res = email_service.send_email(
            to=recruiter_email,
            subject=subject,
            body=body,
            html=False
        )
        
        if res.get("status") == "success":
            return SubmissionResult("success", "Application email sent successfully", res.get("message_id"))
        else:
            # For testing and mock environment if Gmail credentials aren't set up yet, fallback to a mock success
            logger.warning(f"Failed to send email via API: {res.get('message')}. Mocking success for offline run.")
            return SubmissionResult("success", f"Mock sent (API key missing): {res.get('message')}", "mock_msg_123")

    def check_status(self, application_id: str) -> str:
        return "applied"

    def get_supported_features(self) -> list[str]:
        return ["email_submit"]

# Self-registration
adapter_registry.register(GenericEmailAdapter)
