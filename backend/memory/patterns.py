from backend.core.database import SessionLocal
from backend.memory.models import AgentMemory

class PatternExtractor:
    def get_patterns(self, agent_id: str, memory_type: str) -> list:
        db = SessionLocal()
        try:
            # MVP: just return all memories of that type as patterns
            # In a full version, we'd use an LLM to aggregate and summarize
            memories = db.query(AgentMemory).filter(
                AgentMemory.agent_id == agent_id,
                AgentMemory.memory_type == memory_type
            ).order_by(AgentMemory.relevance_score.desc()).limit(10).all()
            
            return [mem.content for mem in memories]
        finally:
            db.close()

pattern_extractor = PatternExtractor()
