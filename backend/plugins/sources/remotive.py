from backend.plugins.base import BaseSourcePlugin
from backend.plugins.registry import registry
import requests

class RemotiveSourcePlugin(BaseSourcePlugin):
    name = "remotive"

    def __init__(self):
        self.base_url = "https://remotive.com/api/remote-jobs"

    def search_jobs(self, filters: dict) -> list:
        keyword = filters.get("keyword", "software engineer")
        params = {
            "search": keyword,
            "limit": 20
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Failed to fetch from Remotive API: {e}. Returning mock data.")
            return [
                {
                    "external_id": "rem_mock_1",
                    "title": "Backend Engineer",
                    "company_name": "CloudSystems",
                    "location": "Worldwide",
                    "description": "Looking for a Go/Python developer.",
                    "url": "https://remotive.com/jobs/mock1"
                }
            ]

        jobs = []
        for item in data.get("jobs", []):
            jobs.append({
                "external_id": str(item.get("id")),
                "title": item.get("title"),
                "company_name": item.get("company_name"),
                "location": item.get("candidate_required_location", "Remote"),
                "description": item.get("description"),
                "url": item.get("url")
            })

        return jobs

    def get_job_details(self, job_id: str) -> dict:
        # Remotive returns all details in list, no detail endpoint needed
        raise NotImplementedError("Remotive does not have a direct detail API")

# Register
registry.register_source(RemotiveSourcePlugin)
