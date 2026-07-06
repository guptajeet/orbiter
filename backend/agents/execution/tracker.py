import logging
from backend.agents.base import BaseAgent

logger = logging.getLogger(__name__)

class TrackingAgent(BaseAgent):
    def __init__(self):
        super().__init__("tracker")

    def process(self, task: dict):
        if task.get("type") != "track_application":
            return {"status": "ignored"}
            
        application_id = task.get("application_id")
        
        try:
            # MVP: Just mock tracking status update
            logger.info(f"Tracking agent checking status for {application_id}")
            return {"status": "success", "application_status": "in_review"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

tracking_agent = TrackingAgent()
