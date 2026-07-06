import datetime
from backend.core.database import SessionLocal
from backend.memory.models import AgentMemory

class MemoryDecay:
    def decay_memories(self):
        """Reduces relevance score over time for rarely accessed memories"""
        db = SessionLocal()
        try:
            now = datetime.datetime.utcnow()
            all_memories = db.query(AgentMemory).all()
            for mem in all_memories:
                days_since_access = (now - mem.last_accessed_at).days
                if days_since_access > 30:
                    # Decay 10% for every month not accessed
                    decay_factor = 0.9 ** (days_since_access / 30)
                    mem.relevance_score = max(0.1, mem.relevance_score * decay_factor)
            db.commit()
        finally:
            db.close()

memory_decay = MemoryDecay()
