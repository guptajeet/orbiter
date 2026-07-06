import hashlib

class Deduplicator:
    def compute_hash(self, data: dict) -> str:
        """Compute a dedup hash from job data"""
        key = f"{data.get('title', '')}|{data.get('company_name', '')}|{data.get('url', '')}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    def is_duplicate(self, dedup_hash: str, existing_hashes: set) -> bool:
        return dedup_hash in existing_hashes

deduplicator = Deduplicator()
