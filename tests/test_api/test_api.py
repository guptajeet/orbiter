import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}

def test_api_dashboard_metrics():
    response = client.get("/api/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "new_matches" in data
    assert "auto_applied" in data
    assert "agent_status" in data
    assert data["agent_status"]["master"] == "online"
