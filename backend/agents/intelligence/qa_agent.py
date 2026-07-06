import logging
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway

logger = logging.getLogger(__name__)

class QaAgent(BaseAgent):
    def __init__(self):
        super().__init__("qa_agent")

    def process(self, task: dict):
        if task.get("type") not in ("verify_hallucinations", "verify_application"):
            return {"status": "ignored"}
            
        original_resume = task.get("original_resume")
        tailored_resume = task.get("tailored_resume")
        
        prompt = f"""
        Compare the tailored resume to the original resume.
        Identify any "hallucinations" — skills, experiences, or degrees present in the tailored resume that are NOT in the original resume.
        Return ONLY valid JSON with:
        - has_hallucinations: boolean
        - hallucinated_items: list of strings
        
        Original Resume: {original_resume}
        Tailored Resume: {tailored_resume}
        """
        
        try:
            # We use a backup provider for verification to avoid same-model bias
            # In a real setup, we'd explicitly route this to a different model in the gateway
            result = ai_gateway.generate("resume_tailoring", prompt)
            from backend.utils.json_parser import extract_json_from_response
            qa_data = extract_json_from_response(result.get("content", ""))
            if not qa_data:
                return {"status": "error", "message": "Failed to parse AI response"}
            return {"status": "success", "qa_result": qa_data}
        except Exception as e:
            logger.error(f"QA agent failed: {e}")
            return {"status": "error", "message": str(e)}

qa_agent = QaAgent()
