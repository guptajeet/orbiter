from backend.agents.base import BaseSupervisor
from .api_apply import api_apply_agent
from .email_apply import email_apply_agent
from .tracker import tracking_agent

class ExecutionSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__("execution")
        self.register_agent(api_apply_agent)
        self.register_agent(email_apply_agent)
        self.register_agent(tracking_agent)

execution_supervisor = ExecutionSupervisor()
