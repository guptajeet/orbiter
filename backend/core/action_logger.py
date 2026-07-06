import uuid
from backend.core.database import SessionLocal
from backend.models.action_log import ActionLog


def log_action(agent_id, action_type, input_summary, output_summary, model_used=None, model_provider=None, confidence_score=None, duration_ms=None):
    db = SessionLocal()
    try:
        entry = ActionLog(
            id=str(uuid.uuid4()),
            agent_id=agent_id,
            action_type=action_type,
            input_summary=input_summary,
            output_summary=output_summary,
            model_used=model_used,
            model_provider=model_provider,
            confidence_score=confidence_score,
            duration_ms=duration_ms,
        )
        db.add(entry)
        db.commit()
        return entry
    finally:
        db.close()


class _ActionLogger:
    def log(self, agent_id, action_type, input_summary, output_summary, model_used=None, model_provider=None, confidence_score=None, duration_ms=None):
        return log_action(agent_id, action_type, input_summary, output_summary, model_used=model_used, model_provider=model_provider, confidence_score=confidence_score, duration_ms=duration_ms)


action_logger = _ActionLogger()
