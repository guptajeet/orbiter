import os
import requests
from .base import BaseATSAdapter, SubmissionResult
from .registry import adapter_registry

class GreenhouseAdapter(BaseATSAdapter):
    name = "greenhouse"
    
    def __init__(self):
        self.api_key = os.getenv("GREENHOUSE_API_KEY")

    def submit_application(self, application_data: dict, resume: str, cover_letter: str) -> SubmissionResult:
        if not self.api_key:
            return SubmissionResult("error", "Greenhouse API key not configured")
            
        # In MVP, we mock the actual submission since we don't have a specific board token
        print(f"Mock submitting to Greenhouse: {application_data.get('job_id')}")
        return SubmissionResult("success", "Application submitted via Greenhouse mock", "gh_12345")

    def check_status(self, application_id: str) -> str:
        return "pending"

    def get_supported_features(self) -> list[str]:
        return ["api_submit", "status_check"]

adapter_registry.register(GreenhouseAdapter)
