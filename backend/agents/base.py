from abc import ABC, abstractmethod
import logging
import traceback
from backend.core import events
from backend.core.automation_mode import mode_engine

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.event_bus = events.event_bus
        self.mode_engine = mode_engine

    @abstractmethod
    def process(self, task: dict):
        pass

    def health_check(self) -> dict:
        return {"status": "ok", "agent_id": self.agent_id}

    def safe_execute(self, action: str, func, *args, **kwargs):
        if not self.mode_engine.can_execute(self.agent_id, action):
            logger.info(f"Agent {self.agent_id} action '{action}' requires approval (Mode: {self.mode_engine.global_mode})")
            return {"status": "queued_for_approval", "action": action}
            
        try:
            result = func(*args, **kwargs)
            return {"status": "success", "result": result}
        except Exception as e:
            logger.error(f"Agent {self.agent_id} failed on action '{action}': {traceback.format_exc()}")
            return {"status": "error", "message": str(e)}

class BaseSupervisor(BaseAgent):
    def __init__(self, supervisor_id: str):
        super().__init__(supervisor_id)
        self.child_agents = {}

    def register_agent(self, agent: BaseAgent):
        self.child_agents[agent.agent_id] = agent

    def process(self, task: dict):
        # Default behavior: route task to specific child agent
        target_agent = task.get("target_agent")
        if target_agent and target_agent in self.child_agents:
            return self.child_agents[target_agent].process(task)
        else:
            return {"error": f"Target agent {target_agent} not found"}
