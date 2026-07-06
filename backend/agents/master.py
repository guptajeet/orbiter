import logging
from backend.agents.base import BaseAgent
from backend.core.events import event_bus

logger = logging.getLogger(__name__)

class MasterOrchestrator(BaseAgent):
    def __init__(self):
        super().__init__("master")
        self.supervisors = {}

    def register_supervisor(self, supervisor_id: str, supervisor_instance):
        self.supervisors[supervisor_id] = supervisor_instance

    def process(self, task: dict):
        task_type = task.get("type")
        
        if task_type == "new_job_found":
            # Route to Intelligence Supervisor for matching
            logger.info(f"Master routing new job to intelligence: {task.get('job_id')}")
            return self.supervisors.get("intelligence").process(task)
            
        elif task_type == "match_completed":
            confidence = task.get("confidence", 0)
            threshold = self.mode_engine.get_threshold()
            
            if confidence >= threshold:
                logger.info(f"High confidence match ({confidence}). Routing to composition.")
                return self.supervisors.get("composition").process(task)
            else:
                logger.info(f"Low/Medium confidence match ({confidence}). Queueing for digest.")
                # Send to reporting supervisor for daily digest
                return self.supervisors.get("reporting").process(task)
                
        else:
            logger.warning(f"Master received unknown task type: {task_type}")
            return {"status": "ignored"}

master = MasterOrchestrator()
