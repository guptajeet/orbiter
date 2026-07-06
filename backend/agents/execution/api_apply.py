import logging
from backend.agents.base import BaseAgent
from backend.adapters.registry import adapter_registry

logger = logging.getLogger(__name__)

class ApiApplyAgent(BaseAgent):
    def __init__(self):
        super().__init__("api_apply")

    def process(self, task: dict):
        if task.get("type") != "submit_application":
            return {"status": "ignored"}
            
        ats_type = task.get("ats_type")
        application_data = task.get("application_data")
        resume_text = task.get("resume_text")
        cover_letter = task.get("cover_letter")
        
        adapter_class = adapter_registry.get_adapter(ats_type)
        if not adapter_class:
            return {"status": "error", "message": f"No adapter found for ATS: {ats_type}"}
            
        try:
            adapter = adapter_class()
            # Check automation mode
            result = self.safe_execute("submit", adapter.submit_application, application_data, resume_text, cover_letter)
            
            if result.get("status") == "success":
                sub_result = result.get("result")
                return {
                    "status": "success",
                    "application_id": sub_result.application_id,
                    "message": sub_result.message
                }
            return result
        except Exception as e:
            logger.error(f"API apply agent failed: {e}")
            return {"status": "error", "message": str(e)}

api_apply_agent = ApiApplyAgent()
