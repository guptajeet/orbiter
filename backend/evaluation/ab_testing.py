import uuid
from backend.core.database import SessionLocal
from backend.evaluation.models import ExperimentResult

class ExperimentManager:
    def record_result(self, experiment_id: str, variant_name: str, outcome: float):
        db = SessionLocal()
        try:
            res = ExperimentResult(
                id=str(uuid.uuid4()),
                experiment_id=experiment_id,
                variant_name=variant_name,
                outcome_value=outcome
            )
            db.add(res)
            db.commit()
            return res.id
        finally:
            db.close()

ab_testing = ExperimentManager()
