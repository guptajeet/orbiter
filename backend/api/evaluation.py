from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.evaluation.models import EvaluationMetric
from backend.evaluation.tracker import metrics_tracker
from backend.evaluation.reporter import evaluation_reporter

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.get("/evaluation/metrics")
def list_metrics(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    metrics = (
        db.query(EvaluationMetric)
        .order_by(EvaluationMetric.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {
        "total": db.query(EvaluationMetric).count(),
        "metrics": [
            {
                "id": m.id,
                "metric_name": m.metric_name,
                "value": m.value,
                "context": m.context,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in metrics
        ],
    }


@router.get("/evaluation/report")
def get_weekly_report():
    report = evaluation_reporter.generate()
    return {"report": report}
