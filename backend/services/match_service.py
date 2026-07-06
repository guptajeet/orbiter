import uuid
from backend.core.database import SessionLocal
from backend.models.match import MatchResult

class MatchService:
    def get_matches(self, limit: int = 50):
        db = SessionLocal()
        try:
            return db.query(MatchResult).order_by(MatchResult.generated_at.desc()).limit(limit).all()
        finally:
            db.close()
    
    def get_match(self, match_id: str):
        db = SessionLocal()
        try:
            return db.query(MatchResult).filter(MatchResult.id == match_id).first()
        finally:
            db.close()
    
    def create_match(self, resume_id: str, job_id: str, scores: dict) -> str:
        db = SessionLocal()
        try:
            match = MatchResult(
                id=str(uuid.uuid4()),
                resume_id=resume_id,
                job_id=job_id,
                **scores
            )
            db.add(match)
            db.commit()
            return match.id
        finally:
            db.close()
    
    def get_count(self) -> int:
        db = SessionLocal()
        try:
            return db.query(MatchResult).count()
        finally:
            db.close()

match_service = MatchService()
