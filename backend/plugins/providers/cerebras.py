from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os
import requests

class CerebrasProvider(BaseProviderPlugin):
    name = "cerebras"

    def __init__(self):
        self.api_key = os.getenv("CEREBRAS_API_KEY")
        self.base_url = "https://api.cerebras.ai/v1/chat/completions"

    def generate(self, prompt: str, **kwargs) -> dict:
        if not self.api_key:
            raise Exception("CEREBRAS_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3.1-8b",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        return {
            "content": result["choices"][0]["message"]["content"],
            "model": "llama3.1-8b"
        }

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embed not supported for Cerebras")

    def get_capabilities(self) -> list[str]:
        return ["generate", "classify"]

# Register
registry.register_provider(CerebrasProvider)
