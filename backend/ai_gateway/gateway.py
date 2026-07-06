import logging
from backend.core.config import settings
from backend.plugins.registry import registry
from .rate_limiter import rate_limiter

logger = logging.getLogger(__name__)

class AIGateway:
    def __init__(self):
        pass

    def _get_config(self):
        if hasattr(self, "config") and self.config is not None:
            return self.config
        return settings.ai_providers

    def generate(self, function_name: str, prompt: str, **kwargs) -> dict:
        config = self._get_config()
        func_config = config.get("functions", {}).get(function_name, {})
        primary = func_config.get("primary")
        backups = func_config.get("backups", [])

        providers_to_try = [primary] + backups if primary else backups
        logger.info(f"AIGateway.generate({function_name}): trying providers {providers_to_try}")

        last_error = None
        for provider_name in providers_to_try:
            if not provider_name:
                continue

            if not rate_limiter.check_limit(provider_name):
                logger.warning(f"AIGateway: skipping {provider_name} (rate limited locally)")
                last_error = Exception(f"Provider {provider_name} rate limited locally")
                continue

            provider_class = registry.get_provider(provider_name)
            if not provider_class:
                logger.warning(f"AIGateway: skipping {provider_name} (not in registry)")
                last_error = Exception(f"Provider {provider_name} not found in plugin registry")
                continue

            try:
                logger.info(f"AIGateway: trying {provider_name} for {function_name}")
                provider_instance = provider_class()
                result = provider_instance.generate(prompt, **kwargs)
                logger.info(f"AIGateway: {provider_name} succeeded for {function_name}")
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"AIGateway: {provider_name} failed: {e}")
                continue

        raise Exception(f"All providers {providers_to_try} failed for {function_name}. Last error: {last_error}")

    def embed(self, function_name: str, text: str) -> list[float]:
        config = self._get_config()
        func_config = config.get("functions", {}).get(function_name, {})
        primary = func_config.get("primary", "huggingface")

        provider_class = registry.get_provider(primary)
        if provider_class:
            return provider_class().embed(text)
        return []

ai_gateway = AIGateway()
