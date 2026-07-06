from backend.ai_gateway.gateway import ai_gateway

class EmbeddingService:
    def get_embedding(self, text: str) -> list[float]:
        try:
            return ai_gateway.embed("embedding", text)
        except Exception:
            return []
    
    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

embedding_service = EmbeddingService()
