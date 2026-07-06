import pytest
from backend.evaluation.models import EvaluationMetric
from backend.evaluation.tracker import metrics_tracker

def test_record_metric(db_session):
    # Override SessionLocal to use test db_session
    import backend.evaluation.tracker as tracker
    tracker.SessionLocal = lambda: db_session

    metric_id = metrics_tracker.record_metric(
        metric_name="callback_rate",
        value=1.0,
        context={"variant": "cover_letter_v2"}
    )
    
    assert metric_id is not None

    # Retrieve and check
    metric = db_session.query(EvaluationMetric).filter(EvaluationMetric.id == metric_id).first()
    assert metric is not None
    assert metric.metric_name == "callback_rate"
    assert metric.value == 1.0
    assert metric.context == {"variant": "cover_letter_v2"}
