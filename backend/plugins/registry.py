from typing import Dict, Any, Type
from .base import BasePlugin, BaseSourcePlugin, BaseProviderPlugin, BaseChannelPlugin

class PluginRegistry:
    def __init__(self):
        self.sources: Dict[str, Type[BaseSourcePlugin]] = {}
        self.providers: Dict[str, Type[BaseProviderPlugin]] = {}
        self.channels: Dict[str, Type[BaseChannelPlugin]] = {}

    def register_source(self, plugin: Type[BaseSourcePlugin]):
        self.sources[plugin.name] = plugin

    def register_provider(self, plugin: Type[BaseProviderPlugin]):
        self.providers[plugin.name] = plugin

    def register_channel(self, plugin: Type[BaseChannelPlugin]):
        self.channels[plugin.name] = plugin

    def get_source(self, name: str) -> Type[BaseSourcePlugin]:
        return self.sources.get(name)

    def get_provider(self, name: str) -> Type[BaseProviderPlugin]:
        return self.providers.get(name)

    def get_channel(self, name: str) -> Type[BaseChannelPlugin]:
        return self.channels.get(name)

registry = PluginRegistry()
