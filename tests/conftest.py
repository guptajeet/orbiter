import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment variables
os.environ["ORBITER_CONFIG_DIR"] = str(Path(__file__).parent.parent / "config")
os.environ["GREENHOUSE_API_KEY"] = "mock_greenhouse_key"
os.environ["WORKDAY_USERNAME"] = "mock_username"
os.environ["WORKDAY_PASSWORD"] = "mock_password"

# Load plugins for all tests
from backend.plugins.manager import plugin_manager
plugin_manager.load_plugins()

from backend.models.base import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def mock_event_bus(monkeypatch):
    from backend.core.events import event_bus
    
    events_list = []
    
    def mock_publish(channel, event_type, payload):
        events_list.append((channel, event_type, payload))
        
    def mock_subscribe(channel):
        return None
        
    monkeypatch.setattr(event_bus, "publish", mock_publish)
    monkeypatch.setattr(event_bus, "subscribe", mock_subscribe)
    monkeypatch.setattr(event_bus, "events", events_list, raising=False)
    return event_bus

@pytest.fixture
def mock_ai_gateway(monkeypatch):
    from backend.ai_gateway.gateway import ai_gateway
    
    def mock_generate(function_name, prompt, **kwargs):
        return {
            "content": '{"score": 0.85, "confidence_tier": "high", "scenario_classification": "exact_match"}',
            "model": "mock-model"
        }
        
    def mock_embed(function_name, text):
        return [0.1] * 384
        
    monkeypatch.setattr(ai_gateway, "generate", mock_generate)
    monkeypatch.setattr(ai_gateway, "embed", mock_embed)
    return ai_gateway
