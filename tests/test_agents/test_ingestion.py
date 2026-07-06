import pytest
from backend.agents.ingestion.api_source import ApiSourceAgent
from backend.models.job import JobListing

def test_api_source_agent_ignored():
    agent = ApiSourceAgent()
    res = agent.process({"type": "invalid_task"})
    assert res == {"status": "ignored"}

def test_api_source_agent_discover_jobs(db_session, mock_event_bus):
    agent = ApiSourceAgent()
    # Temporarily override SessionLocal to return our in-memory db_session
    import backend.agents.ingestion.api_source as api_source
    api_source.SessionLocal = lambda: db_session

    task = {
        "type": "discover_jobs",
        "filters": {"keyword": "python"}
    }
    
    res = agent.process(task)
    assert res["status"] == "success"
    assert len(res["summary"]) > 0
    
    # Check if job listing was created in DB
    jobs = db_session.query(JobListing).all()
    assert len(jobs) > 0
    
    # Check if event was published
    assert len(mock_event_bus.events) > 0
    channel, event_type, payload = mock_event_bus.events[0]
    assert channel == "jobs"
    assert event_type == "new_job_found"
    assert "job_id" in payload
