from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os
import requests

class HuggingFaceProvider(BaseProviderPlugin):
    name = "huggingface"
    
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    def generate(self, prompt: str, **kwargs) -> dict:
        raise NotImplementedError("Generate not implemented for HF MVP")

    def embed(self, text: str) -> list[float]:
        if not self.api_key:
            raise Exception("HUGGINGFACE_API_KEY not configured")
            
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.api_url, headers=headers, json={"inputs": text})
        response.raise_for_status()
        return response.json()

    def get_capabilities(self) -> list[str]:
        return ["embed"]

# Register itself
registry.register_provider(HuggingFaceProvider)
