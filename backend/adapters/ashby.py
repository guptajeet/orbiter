import os
from .base import BaseATSAdapter, SubmissionResult
from .registry import adapter_registry

class AshbyAdapter(BaseATSAdapter):
    name = "ashby"
    
    def submit_application(self, application_data: dict, resume: str, cover_letter: str) -> SubmissionResult:
        print(f"Mock submitting to Ashby: {application_data.get('job_id')}")
        return SubmissionResult("success", "Application submitted via Ashby mock", "as_12345")

    def check_status(self, application_id: str) -> str:
        return "pending"

    def get_supported_features(self) -> list[str]:
        return ["api_submit"]

adapter_registry.register(AshbyAdapter)
