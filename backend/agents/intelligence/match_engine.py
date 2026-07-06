import logging
import uuid
from backend.agents.base import BaseAgent
from backend.ai_gateway.gateway import ai_gateway
from backend.core.database import SessionLocal
from backend.models.job import JobListing
from backend.models.resume import ResumeProfile
from backend.models.match import MatchResult

logger = logging.getLogger(__name__)

class MatchEngineAgent(BaseAgent):
    def __init__(self):
        super().__init__("match_engine")

    def process(self, task: dict):
        if task.get("type") != "match_job":
            return {"status": "ignored"}
            
        job_id = task.get("job_id")
        resume_id = task.get("resume_id")
        
        if not job_id or not resume_id:
            return {"status": "error", "message": "job_id and resume_id required"}
            
        db = SessionLocal()
        try:
            job = db.query(JobListing).filter(JobListing.id == job_id).first()
            resume = db.query(ResumeProfile).filter(ResumeProfile.id == resume_id).first()
            
            if not job or not resume:
                return {"status": "error", "message": "job or resume not found"}
                
            # For MVP, we will use Gemini to generate a score instead of raw cosine similarity
            # In a full production system, we'd do vector math on embeddings first to filter
            prompt = f"""
            Compare this resume to this job description and provide a match score between 0.0 and 1.0.
            Also provide a confidence_tier (high, medium, low, no-fit) and scenario_classification.
            Return ONLY valid JSON.
            
            Resume: {resume.raw_text}
            
            Job: {job.title} at {job.company_name}
            Description: {job.description_raw}
            """
            
            result = ai_gateway.generate("match_scoring", prompt)
            
            from backend.utils.json_parser import extract_json_from_response
            score_data = extract_json_from_response(result.get("content", ""))
            if not score_data:
                return {"status": "error", "message": "Failed to parse AI response"}
            
            overall_score = score_data.get("score", 0.0)
            confidence_tier = score_data.get("confidence_tier", "low")
            if overall_score >= 0.8:
                confidence_tier = "high"
            elif overall_score >= 0.5:
                confidence_tier = "medium"
                
            match = MatchResult(
                id=str(uuid.uuid4()),
                resume_id=resume.id,
                job_id=job.id,
                cosine_similarity=overall_score,  # simplified
                confidence_tier=confidence_tier,
                scenario_classification=score_data.get("scenario_classification", "standard")
            )
            db.add(match)
            db.commit()
            
            # Emit event that match is completed
            self.event_bus.publish("jobs", "match_completed", {
                "match_id": match.id,
                "confidence": overall_score
            })
            
            return {"status": "success", "match_id": match.id, "score": overall_score}
            
        except Exception as e:
            logger.error(f"Match engine failed: {e}")
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()

match_engine_agent = MatchEngineAgent()
