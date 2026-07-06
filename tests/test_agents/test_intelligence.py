import pytest
from backend.agents.intelligence.match_engine import MatchEngineAgent
from backend.models.job import JobListing
from backend.models.resume import ResumeProfile
from backend.models.match import MatchResult

def test_match_engine_ignored():
    agent = MatchEngineAgent()
    res = agent.process({"type": "invalid_task"})
    assert res == {"status": "ignored"}

def test_match_engine_success(db_session, mock_event_bus, mock_ai_gateway):
    # Setup test mock database elements
    resume = ResumeProfile(id="res_1", user_id="user_1", raw_text="Experienced Python FastAPI Developer", is_primary=True)
    job = JobListing(id="job_1", source_type="api", source_name="remotive", external_id="1", url="http://x", company_name="Tech", title="FastAPI dev", description_raw="FastAPI", dedup_hash="x")
    db_session.add(resume)
    db_session.add(job)
    db_session.commit()

    agent = MatchEngineAgent()
    
    # Override SessionLocal to use test db_session
    import backend.agents.intelligence.match_engine as match_engine
    match_engine.SessionLocal = lambda: db_session

    task = {
        "type": "match_job",
        "job_id": "job_1",
        "resume_id": "res_1"
    }

    res = agent.process(task)
    assert res["status"] == "success"
    assert "match_id" in res
    assert res["score"] == 0.85

    # Check match was created in database
    match = db_session.query(MatchResult).filter(MatchResult.id == res["match_id"]).first()
    assert match is not None
    assert match.cosine_similarity == 0.85
    assert match.confidence_tier == "high"

    # Check match completed event was emitted
    assert len(mock_event_bus.events) > 0
    channel, event_type, payload = mock_event_bus.events[0]
    assert channel == "jobs"
    assert event_type == "match_completed"
    assert payload["match_id"] == match.id
    assert payload["confidence"] == 0.85
