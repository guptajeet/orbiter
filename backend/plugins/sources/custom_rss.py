from backend.plugins.base import BaseSourcePlugin
from backend.plugins.registry import registry
import xml.etree.ElementTree as ET
import requests

class CustomRssSourcePlugin(BaseSourcePlugin):
    name = "custom_rss"

    def __init__(self):
        # Fallback feed for mock or default RSS searches
        self.feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"

    def search_jobs(self, filters: dict) -> list:
        url = filters.get("feed_url", self.feed_url)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            xml_data = response.content
            root = ET.fromstring(xml_data)
        except Exception as e:
            print(f"Failed parsing RSS feed at {url}: {e}. Returning mock RSS jobs.")
            return [
                {
                    "external_id": "rss_mock_1",
                    "title": "React Developer",
                    "company_name": "WebStudio",
                    "location": "Remote",
                    "description": "Expert Frontend Developer wanted for React/Next.js projects.",
                    "url": "https://example.com/rss1"
                }
            ]

        jobs = []
        # Standard RSS parses <channel><item>...
        items = root.findall(".//item")
        for idx, item in enumerate(items):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            description = item.findtext("description", "")
            guid = item.findtext("guid", f"rss_{idx}")
            
            # Simple metadata parses from titles (often like "Company Name: Title" in WWR)
            company_name = "RSS Feed Publisher"
            if ":" in title:
                parts = title.split(":", 1)
                company_name = parts[0].strip()
                title = parts[1].strip()

            jobs.append({
                "external_id": guid,
                "title": title,
                "company_name": company_name,
                "location": "Remote",
                "description": description,
                "url": link
            })
            
            # Cap at 20 jobs
            if len(jobs) >= 20:
                break
                
        return jobs

    def get_job_details(self, job_id: str) -> dict:
        raise NotImplementedError("RSS source plugin does not support detail fetches")

# Register
registry.register_source(CustomRssSourcePlugin)
