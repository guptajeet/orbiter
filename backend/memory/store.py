import uuid
import datetime
try:
    import chromadb
except ImportError:
    chromadb = None

from backend.core.database import SessionLocal
from backend.memory.models import AgentMemory
from backend.core.config import settings

class MemoryStore:
    def __init__(self):
        db_path = settings.default_config.get("paths", {}).get("memory_db", "./memory_chroma")
        if chromadb:
            try:
                self.chroma_client = chromadb.PersistentClient(path=db_path)
                self.collection = self.chroma_client.get_or_create_collection(name="agent_memories")
            except Exception:
                self.chroma_client = None
                self.collection = None
        else:
            self.chroma_client = None
            self.collection = None

    def remember(self, agent_id: str, memory_type: str, content: dict, embedding: list[float] = None):
        db = SessionLocal()
        try:
            memory_id = str(uuid.uuid4())
            memory = AgentMemory(
                id=memory_id,
                agent_id=agent_id,
                memory_type=memory_type,
                content=content
            )
            db.add(memory)
            db.commit()
            
            if embedding and self.collection:
                import json
                self.collection.add(
                    embeddings=[embedding],
                    documents=[json.dumps(content)],
                    metadatas=[{"agent_id": agent_id, "memory_type": memory_type}],
                    ids=[memory_id]
                )
            
            return memory_id
        finally:
            db.close()

    def recall(self, agent_id: str, query_embedding: list[float], memory_type: str = None, top_k: int = 5) -> list[AgentMemory]:
        if not self.collection:
            # Fallback: query DB directly if chromadb is not loaded
            db = SessionLocal()
            try:
                query = db.query(AgentMemory).filter(AgentMemory.agent_id == agent_id)
                if memory_type:
                    query = query.filter(AgentMemory.memory_type == memory_type)
                memories = query.limit(top_k).all()
                for mem in memories:
                    mem.access_count += 1
                    mem.last_accessed_at = datetime.datetime.utcnow()
                db.commit()
                return memories
            finally:
                db.close()

        where_clause = {"agent_id": agent_id}
        if memory_type:
            where_clause["memory_type"] = memory_type
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause
        )
        
        db = SessionLocal()
        try:
            memories = []
            if results and results.get("ids") and len(results["ids"]) > 0:
                for memory_id in results["ids"][0]:
                    mem = db.query(AgentMemory).filter(AgentMemory.id == memory_id).first()
                    if mem:
                        mem.access_count += 1
                        mem.last_accessed_at = datetime.datetime.utcnow()
                        memories.append(mem)
                db.commit()
            return memories
        finally:
            db.close()

memory_store = MemoryStore()
