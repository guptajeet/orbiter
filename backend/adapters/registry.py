from typing import Dict, Type
from .base import BaseATSAdapter

class AdapterRegistry:
    def __init__(self):
        self.adapters: Dict[str, Type[BaseATSAdapter]] = {}

    def register(self, adapter: Type[BaseATSAdapter]):
        self.adapters[adapter.name] = adapter

    def get_adapter(self, name: str) -> Type[BaseATSAdapter]:
        return self.adapters.get(name)

adapter_registry = AdapterRegistry()
