import os
import json
import logging

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self.client = None
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            import redis
            self.client = redis.Redis.from_url(redis_url, socket_connect_timeout=2)
            self.client.ping()
        except Exception:
            self.client = None

    def publish(self, channel: str, event_type: str, payload: dict):
        if not self.client:
            return
        try:
            message = {"type": event_type, "payload": payload}
            self.client.publish(channel, json.dumps(message))
        except Exception:
            self.client = None

    def subscribe(self, channel: str):
        if not self.client:
            return None
        try:
            pubsub = self.client.pubsub()
            pubsub.subscribe(channel)
            return pubsub
        except Exception:
            return None

event_bus = EventBus()
