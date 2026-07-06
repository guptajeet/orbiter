from backend.evaluation.reporter import evaluation_reporter
from backend.core.database import SessionLocal
from backend.models.action_log import ActionLog

class AnalyticsService:
    def get_agent_activity(self, limit: int = 50):
        db = SessionLocal()
        try:
            logs = db.query(ActionLog).order_by(ActionLog.created_at.desc()).limit(limit).all()
            return [{
                "agent_id": log.agent_id,
                "action_type": log.action_type,
                "model_used": log.model_used,
                "confidence_score": log.confidence_score,
                "created_at": log.created_at.isoformat() if log.created_at else None,
                "duration_ms": log.duration_ms
            } for log in logs]
        finally:
            db.close()
    
    def get_summary(self) -> dict:
        return evaluation_reporter.generate()

analytics_service = AnalyticsService()
