from backend.plugins.base import BaseSourcePlugin
from backend.plugins.registry import registry
import os
import requests

class AdzunaSourcePlugin(BaseSourcePlugin):
    name = "adzuna"
    
    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID")
        self.app_key = os.getenv("ADZUNA_APP_KEY")
        self.base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    def search_jobs(self, filters: dict) -> list:
        if not self.app_id or not self.app_key:
            print("Adzuna API credentials not configured. Returning mock data.")
            return [
                {
                    "external_id": "adz_mock_1",
                    "title": "Software Engineer",
                    "company_name": "TechCorp",
                    "location": "Remote",
                    "description": "Looking for a Python/FastAPI engineer.",
                    "url": "https://example.com/job1"
                }
            ]
            
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": filters.get("keyword", "software engineer"),
            "where": filters.get("location", "remote"),
            "results_per_page": 20
        }
        
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for item in data.get("results", []):
            jobs.append({
                "external_id": str(item.get("id")),
                "title": item.get("title"),
                "company_name": item.get("company", {}).get("display_name"),
                "location": item.get("location", {}).get("display_name"),
                "description": item.get("description"),
                "url": item.get("redirect_url")
            })
            
        return jobs

    def get_job_details(self, job_id: str) -> dict:
        raise NotImplementedError("Adzuna doesn't provide a direct job detail endpoint in the same way")

# Register itself
registry.register_source(AdzunaSourcePlugin)
