from backend.core.database import SessionLocal
from backend.promptops.models import PromptVersion

class PromptMetrics:
    def log_invocation(self, version_id: str, latency_ms: float, cost: float, quality_score: float = None):
        db = SessionLocal()
        try:
            pv = db.query(PromptVersion).filter(PromptVersion.id == version_id).first()
            if pv:
                metrics = pv.performance_metrics or {}
                count = metrics.get("total_invocations", 0)
                avg_lat = metrics.get("avg_latency_ms", 0.0)
                
                # Moving average
                metrics["avg_latency_ms"] = ((avg_lat * count) + latency_ms) / (count + 1)
                metrics["total_invocations"] = count + 1
                
                pv.performance_metrics = metrics
                db.commit()
        finally:
            db.close()

prompt_metrics = PromptMetrics()
