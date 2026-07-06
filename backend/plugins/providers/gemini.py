from backend.plugins.base import BaseProviderPlugin
from backend.plugins.registry import registry
import os

class GeminiProvider(BaseProviderPlugin):
    name = "gemini"
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                self.model_name = "gemini-2.0-flash"
            except ImportError:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.client = None
                self.model = genai.GenerativeModel("gemini-2.0-flash")
            self.use_new_client = hasattr(self, 'client') and self.client is not None
        else:
            self.model = None
            self.client = None
            self.use_new_client = False

    def generate(self, prompt: str, **kwargs) -> dict:
        if not self.client and not self.model:
            raise Exception("GEMINI_API_KEY not configured")
        if self.use_new_client:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
            return {"content": response.text, "model": self.model_name}
        else:
            response = self.model.generate_content(prompt)
            return {"content": response.text, "model": "gemini-2.0-flash"}

    def embed(self, text: str) -> list[float]:
        if not self.client and not self.model:
            raise Exception("GEMINI_API_KEY not configured")
        if self.use_new_client:
            response = self.client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            if hasattr(response, 'embeddings') and response.embeddings:
                return response.embeddings[0].values
            elif hasattr(response, 'embedding') and hasattr(response.embedding, 'values'):
                return response.embedding.values
            raise Exception("Failed to parse embedding response from Gemini")
        else:
            import google.generativeai as genai
            response = genai.embed_content(
                model="models/text-embedding-004",
                contents=text
            )
            return response['embedding']

    def get_capabilities(self) -> list[str]:
        return ["generate", "classify", "embed"]

# Register itself
registry.register_provider(GeminiProvider)
