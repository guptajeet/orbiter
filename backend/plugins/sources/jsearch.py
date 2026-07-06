from backend.plugins.base import BaseSourcePlugin
from backend.plugins.registry import registry

class JSearchSourcePlugin(BaseSourcePlugin):
    name = "jsearch"
    
    def search_jobs(self, filters: dict) -> list:
        # Mocking for MVP since RapidAPI JSearch requires complex auth
        print("JSearch mock searching...")
        return [
            {
                "external_id": "js_mock_1",
                "title": "Backend Developer",
                "company_name": "DataWorks",
                "location": "New York, NY",
                "description": "We need a strong backend dev with Python skills.",
                "url": "https://example.com/job2"
            }
        ]

    def get_job_details(self, job_id: str) -> dict:
        return {}

# Register itself
registry.register_source(JSearchSourcePlugin)
