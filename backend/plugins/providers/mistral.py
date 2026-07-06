from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os
import requests

class MistralProvider(BaseProviderPlugin):
    name = "mistral"

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.base_url = "https://api.mistral.ai/v1/chat/completions"

    def generate(self, prompt: str, **kwargs) -> dict:
        if not self.api_key:
            raise Exception("MISTRAL_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-tiny",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        return {
            "content": result["choices"][0]["message"]["content"],
            "model": "mistral-tiny"
        }

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embed not supported for Mistral")

    def get_capabilities(self) -> list[str]:
        return ["generate", "classify"]

# Register
registry.register_provider(MistralProvider)
