import logging
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway

logger = logging.getLogger(__name__)

class ResumeTailorAgent(BaseAgent):
    def __init__(self):
        super().__init__("resume_tailor")

    def process(self, task: dict):
        if task.get("type") != "tailor_resume":
            return {"status": "ignored"}
            
        original_resume = task.get("resume_text")
        job_description = task.get("job_description")
        
        prompt = f"""
        Tailor the provided resume to better match the job description.
        Highlight relevant skills and experiences. DO NOT fabricate any facts.
        Return the tailored resume in Markdown format.
        
        Original Resume: {original_resume}
        Job Description: {job_description}
        """
        
        try:
            # Check mode before executing
            result = self.safe_execute("compose", ai_gateway.generate, "resume_tailoring", prompt)
            
            if result.get("status") == "success":
                tailored_content = result.get("result", {}).get("content", "")
                return {"status": "success", "tailored_resume": tailored_content}
            else:
                return result
                
        except Exception as e:
            logger.error(f"Resume tailor agent failed: {e}")
            return {"status": "error", "message": str(e)}

resume_tailor_agent = ResumeTailorAgent()
