from backend.core.database import SessionLocal
from backend.evaluation.models import EvaluationMetric

class StatisticalAnalyzer:
    def calculate_average(self, metric_name: str) -> float:
        db = SessionLocal()
        try:
            metrics = db.query(EvaluationMetric).filter(
                EvaluationMetric.metric_name == metric_name
            ).all()
            
            if not metrics:
                return 0.0
                
            total = sum(m.value for m in metrics)
            return total / len(metrics)
        finally:
            db.close()

statistical_analyzer = StatisticalAnalyzer()
