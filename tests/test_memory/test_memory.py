import pytest
from backend.memory.models import AgentMemory
from backend.memory.store import MemoryStore

def test_memory_store_remember(db_session):
    # Mock chromadb persistent client
    class MockCollection:
        def __init__(self):
            self.added = []
        def add(self, embeddings, documents, metadatas, ids):
            self.added.append((embeddings, documents, metadatas, ids))
            
    class MockClient:
        def get_or_create_collection(self, name):
            return MockCollection()
            
    # Override SessionLocal to use test db_session
    import backend.memory.store as store
    store.SessionLocal = lambda: db_session

    m_store = store.MemoryStore()
    m_store.chroma_client = MockClient()
    m_store.collection = MockCollection()
    
    memory_id = m_store.remember(
        agent_id="test_agent",
        memory_type="user_preference",
        content={"key": "value"},
        embedding=[0.1] * 384
    )
    
    assert memory_id is not None
    assert len(m_store.collection.added) == 1
    
    # Check it exists in DB
    mem = db_session.query(AgentMemory).filter(AgentMemory.id == memory_id).first()
    assert mem is not None
    assert mem.agent_id == "test_agent"
    assert mem.content == {"key": "value"}
