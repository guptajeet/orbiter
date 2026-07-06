from backend.agents.base import BaseSupervisor
from .api_source import api_source_agent
from .email_monitor import email_monitor_agent

class IngestionSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__("ingestion")
        self.register_agent(api_source_agent)
        self.register_agent(email_monitor_agent)

    def trigger_discovery(self, filters: dict = None):
        return api_source_agent.process({"type": "discover_jobs", "filters": filters or {}})

ingestion_supervisor = IngestionSupervisor()
