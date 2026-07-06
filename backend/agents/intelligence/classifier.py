import logging
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway

logger = logging.getLogger(__name__)

class ClassificationAgent(BaseAgent):
    def __init__(self):
        super().__init__("classifier")

    def process(self, task: dict):
        if task.get("type") not in ("classify_scenario", "classify_job"):
            return {"status": "ignored"}
            
        resume_text = task.get("resume_text")
        job_description = task.get("job_description")
        
        prompt = f"""
        Classify the application scenario into one of the following:
        - standard_match (strong alignment)
        - career_transition (skills match but different title/industry)
        - senior_stretch (applying for a level up)
        - domain_stretch (applying for slightly different sub-domain)
        
        Provide the classification and a brief explanation in JSON format.
        
        Resume: {resume_text}
        Job: {job_description}
        """
        
        try:
            result = ai_gateway.generate("match_scoring", prompt)
            from backend.utils.json_parser import extract_json_from_response
            classification_data = extract_json_from_response(result.get("content", ""))
            if not classification_data:
                return {"status": "error", "message": "Failed to parse AI response"}
            return {"status": "success", "classification": classification_data}
        except Exception as e:
            logger.error(f"Classification agent failed: {e}")
            return {"status": "error", "message": str(e)}

classifier_agent = ClassificationAgent()
