import uuid
from backend.core.database import SessionLocal
from backend.evaluation.models import EvaluationMetric

class MetricsTracker:
    def record_metric(self, metric_name: str, value: float, context: dict = None):
        db = SessionLocal()
        try:
            metric = EvaluationMetric(
                id=str(uuid.uuid4()),
                metric_name=metric_name,
                value=value,
                context=context or {}
            )
            db.add(metric)
            db.commit()
            return metric.id
        finally:
            db.close()

metrics_tracker = MetricsTracker()
