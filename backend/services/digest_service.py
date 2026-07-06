from backend.core.config import settings
from backend.services.job_service import job_service
from backend.services.match_service import match_service
from backend.services.apply_service import apply_service

class DigestService:
    def generate_digest(self) -> dict:
        return {
            "new_matches": match_service.get_count(),
            "auto_applied": apply_service.get_application_count("submitted"),
            "review_needed": apply_service.get_application_count("pending_approval"),
            "total_jobs_discovered": job_service.get_count()
        }

digest_service = DigestService()
