import logging
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway
from backend.core.database import SessionLocal
from backend.models.resume import ResumeProfile
from backend.utils.json_parser import extract_json_from_response

logger = logging.getLogger(__name__)

class ResumeParserAgent(BaseAgent):
    def __init__(self):
        super().__init__("resume_parser")

    def process(self, task: dict):
        if task.get("type") != "parse_resume":
            return {"status": "ignored"}

        raw_text = task.get("raw_text")
        profile_id = task.get("profile_id")
        if not raw_text or not profile_id:
            return {"status": "error", "message": "No raw_text or profile_id provided"}

        prompt = f"""
        Extract the following information from this resume and return ONLY valid JSON:
        - name: string
        - email: string
        - phone: string
        - skills: list of strings
        - experience: list of objects (title, company, start_date, end_date, description)
        - education: list of objects (degree, institution, year)

        Resume Text:
        {raw_text}
        """

        try:
            result = ai_gateway.generate("resume_parsing", prompt)

            json_data = extract_json_from_response(result.get("content", ""))
            if not json_data:
                return {"status": "error", "message": "Failed to parse AI response"}

            embedding = ai_gateway.embed("embedding", raw_text)

            db = SessionLocal()
            try:
                profile = db.query(ResumeProfile).filter(ResumeProfile.id == profile_id).first()
                if profile:
                    profile.parsed_sections = json_data
                    profile.domain_tags = json_data.get("skills", [])
                    profile.label = json_data.get("name", "default")
                    db.commit()
            finally:
                db.close()

            return {
                "status": "success",
                "parsed_data": json_data,
                "embedding_length": len(embedding) if embedding else 0
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

resume_parser_agent = ResumeParserAgent()
