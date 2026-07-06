import datetime
from sqlalchemy import Column, String, Integer, Float, JSON, DateTime
from backend.models.base import Base

class EvaluationMetric(Base):
    __tablename__ = "evaluation_metrics"
    
    id = Column(String, primary_key=True)
    metric_name = Column(String)
    value = Column(Float)
    context = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ExperimentResult(Base):
    __tablename__ = "experiment_results"
    
    id = Column(String, primary_key=True)
    experiment_id = Column(String)
    variant_name = Column(String)
    outcome_value = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
