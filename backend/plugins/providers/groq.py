from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os
import requests

class GroqProvider(BaseProviderPlugin):
    name = "groq"
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str, **kwargs) -> dict:
        if not self.api_key:
            raise Exception("GROQ_API_KEY not configured")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(self.base_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return {"content": result["choices"][0]["message"]["content"], "model": "llama-3.1-8b-instant"}

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Embed not supported for Groq")

    def get_capabilities(self) -> list[str]:
        return ["generate", "classify"]

# Register itself
registry.register_provider(GroqProvider)
