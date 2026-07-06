import pytest
from backend.ai_gateway.gateway import AIGateway

def test_ai_gateway_generate_fallback(monkeypatch):
    # Setup mock registry and configurations
    gw = AIGateway()
    gw.config = {
        "functions": {
            "test_func": {
                "primary": "mock_provider_fail",
                "backups": ["mock_provider_success"]
            }
        }
    }
    
    # Mock registry lookup
    class MockFailProvider:
        def generate(self, prompt, **kwargs):
            raise Exception("Primary provider failure")
            
    class MockSuccessProvider:
        def generate(self, prompt, **kwargs):
            return {"content": "Success content", "model": "success-model"}

    monkeypatch.setattr("backend.ai_gateway.gateway.registry.get_provider", lambda name: (
        MockFailProvider if name == "mock_provider_fail" else MockSuccessProvider
    ))

    # Test that it falls back to success provider
    res = gw.generate("test_func", "hello")
    assert res["content"] == "Success content"
    assert res["model"] == "success-model"
