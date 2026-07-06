from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os
import requests

class OpenRouterProvider(BaseProviderPlugin):
    name = "openrouter"
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def generate(self, prompt: str, **kwargs) -> dict:
        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY not configured")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Orbiter"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return {"content": result["choices"][0]["message"]["content"], "model": data["model"]}

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embed not supported for OpenRouter")

    def get_capabilities(self) -> list[str]:
        return ["generate", "classify"]

# Register itself
registry.register_provider(OpenRouterProvider)
