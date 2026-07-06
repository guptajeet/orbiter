import logging
import importlib
from backend.core.config import settings
from .registry import registry
from .base import BaseSourcePlugin, BaseProviderPlugin, BaseChannelPlugin

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self):
        self.config = settings.plugins_config
        
    def load_plugins(self):
        plugins_conf = self.config.get("plugins", {})
        
        for source_conf in plugins_conf.get("sources", []):
            if source_conf.get("enabled"):
                self._load_module(source_conf.get("module"), "source")
                
        for provider_conf in plugins_conf.get("providers", []):
            if provider_conf.get("enabled"):
                self._load_module(provider_conf.get("module"), "provider")
                
        for channel_conf in plugins_conf.get("channels", []):
            if channel_conf.get("enabled"):
                self._load_module(channel_conf.get("module"), "channel")

    def _load_module(self, module_name: str, plugin_type: str):
        try:
            # We assume the module registers itself upon import
            importlib.import_module(f"backend.{module_name}")
        except Exception as e:
            logger.warning(f"Failed to load plugin {module_name}: {e}")

plugin_manager = PluginManager()
