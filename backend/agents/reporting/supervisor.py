from backend.agents.base import BaseSupervisor
from .digest_agent import digest_agent
from .alert_agent import alert_agent

class ReportingSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__("reporting")
        self.register_agent(digest_agent)
        self.register_agent(alert_agent)

reporting_supervisor = ReportingSupervisor()
