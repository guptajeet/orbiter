import logging
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway

logger = logging.getLogger(__name__)

class CoverLetterAgent(BaseAgent):
    def __init__(self):
        super().__init__("cover_letter")

    def process(self, task: dict):
        if task.get("type") != "generate_cover_letter":
            return {"status": "ignored"}
            
        resume_text = task.get("resume_text")
        job_description = task.get("job_description")
        company_name = task.get("company_name")
        
        prompt = f"""
        Write a professional cover letter for the following job using the applicant's resume.
        Keep it concise, engaging, and highlight the most relevant overlap.
        Return ONLY the cover letter text.
        
        Company: {company_name}
        Resume: {resume_text}
        Job Description: {job_description}
        """
        
        try:
            result = self.safe_execute("compose", ai_gateway.generate, "cover_letter", prompt)
            
            if result.get("status") == "success":
                content = result.get("result", {}).get("content", "")
                return {"status": "success", "cover_letter": content}
            else:
                return result
                
        except Exception as e:
            logger.error(f"Cover letter agent failed: {e}")
            return {"status": "error", "message": str(e)}

cover_letter_agent = CoverLetterAgent()
