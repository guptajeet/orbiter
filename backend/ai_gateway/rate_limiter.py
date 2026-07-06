import time
from backend.core.config import settings
from backend.plugins.registry import registry

class RateLimiter:
    def __init__(self):
        # In a real app, this would use Redis to track across workers
        self.usage = {}
        
    def check_limit(self, provider_name: str) -> bool:
        """Returns True if within limit, False if rate limited"""
        # Simplistic memory rate limiter for MVP
        now = time.time()
        if provider_name not in self.usage:
            self.usage[provider_name] = []
        
        # Clean up old requests (> 60 seconds)
        self.usage[provider_name] = [t for t in self.usage[provider_name] if now - t < 60]
        
        config = settings.ai_providers.get("providers", {}).get(provider_name, {})
        limit = config.get("rate_limit", {}).get("requests_per_minute", 60)
        
        if len(self.usage[provider_name]) >= limit:
            return False
            
        self.usage[provider_name].append(now)
        return True

rate_limiter = RateLimiter()
