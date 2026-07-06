from backend.agents.base import BaseSupervisor
from .resume_parser import resume_parser_agent
from .match_engine import match_engine_agent
from .classifier import classifier_agent
from .qa_agent import qa_agent

class IntelligenceSupervisor(BaseSupervisor):
    def __init__(self):
        super().__init__("intelligence")
        self.register_agent(resume_parser_agent)
        self.register_agent(match_engine_agent)
        self.register_agent(classifier_agent)
        self.register_agent(qa_agent)

intelligence_supervisor = IntelligenceSupervisor()
