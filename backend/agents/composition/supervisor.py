from backend.agents.base import BaseSupervisor
from .resume_tailor import resume_tailor_agent
from .cover_letter import cover_letter_agent

class CompositionSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__("composition")
        self.register_agent(resume_tailor_agent)
        self.register_agent(cover_letter_agent)

composition_supervisor = CompositionSupervisor()
