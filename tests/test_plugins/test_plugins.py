import pytest
from backend.plugins.registry import registry
from backend.plugins.manager import plugin_manager

def test_plugin_manager_loads_all():
    plugin_manager.load_plugins()

    # Sources
    assert registry.get_source("adzuna") is not None
    assert registry.get_source("remotive") is not None
    assert registry.get_source("custom_rss") is not None

    # Providers
    assert registry.get_provider("gemini") is not None
    assert registry.get_provider("groq") is not None
    assert registry.get_provider("huggingface") is not None
    assert registry.get_provider("cerebras") is not None
    assert registry.get_provider("mistral") is not None
    assert registry.get_provider("deepseek") is not None

    # Channels
    assert registry.get_channel("gmail") is not None
    assert registry.get_channel("smtp_generic") is not None

def test_provider_capabilities():
    gemini = registry.get_provider("gemini")()
    assert "generate" in gemini.get_capabilities()
    assert "classify" in gemini.get_capabilities()

    hf = registry.get_provider("huggingface")()
    assert "embed" in hf.get_capabilities()
